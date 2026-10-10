import os
import json
import socket
import logging
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("NeonClient")
logger.setLevel(logging.INFO)

try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


class NeonClient:
    """
    Authoritative client for Neon Serverless PostgreSQL.
    Stores and retrieves structured records for:
    - Deals & normalized profiles
    - Stakeholders & buying committees
    - Deal interactions & timeline events
    - Risk registers & mitigations
    - Multi-vector assessments & scoring models
    - Recommended action items & staging status
    - Multi-turn DIAS session state
    - Generated documents & Workspace links
    """

    SCHEMA_DDL = """
    CREATE TABLE IF NOT EXISTS deals (
        deal_id VARCHAR(100) PRIMARY KEY,
        customer VARCHAR(255) NOT NULL,
        owner VARCHAR(255),
        value NUMERIC(15, 2) DEFAULT 0.00,
        currency VARCHAR(10) DEFAULT 'USD',
        stage VARCHAR(100) DEFAULT 'Discovery',
        budget_status VARCHAR(100) DEFAULT 'Unknown',
        competition VARCHAR(255),
        timeline VARCHAR(100),
        verification_status VARCHAR(50) DEFAULT 'unverified',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS stakeholders (
        id SERIAL PRIMARY KEY,
        deal_id VARCHAR(100) REFERENCES deals(deal_id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        role VARCHAR(100),
        title VARCHAR(255),
        email VARCHAR(255),
        buying_authority VARCHAR(50),
        sentiment VARCHAR(50) DEFAULT 'Neutral',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS deal_interactions (
        id SERIAL PRIMARY KEY,
        deal_id VARCHAR(100) REFERENCES deals(deal_id) ON DELETE CASCADE,
        event_type VARCHAR(100) NOT NULL,
        content TEXT NOT NULL,
        source VARCHAR(100) DEFAULT 'user_input',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS deal_risks (
        id SERIAL PRIMARY KEY,
        deal_id VARCHAR(100) REFERENCES deals(deal_id) ON DELETE CASCADE,
        risk_type VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        severity VARCHAR(50) DEFAULT 'Medium',
        mitigation TEXT,
        status VARCHAR(50) DEFAULT 'Identified',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS deal_assessments (
        id SERIAL PRIMARY KEY,
        deal_id VARCHAR(100) REFERENCES deals(deal_id) ON DELETE CASCADE,
        overall_health NUMERIC(5, 2) NOT NULL,
        win_probability NUMERIC(5, 2) NOT NULL,
        scoring_breakdown JSONB,
        model_version VARCHAR(50) DEFAULT '1.0.0',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS deal_actions (
        id SERIAL PRIMARY KEY,
        deal_id VARCHAR(100) REFERENCES deals(deal_id) ON DELETE CASCADE,
        action_type VARCHAR(100) NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        owner VARCHAR(255),
        due_date VARCHAR(100),
        status VARCHAR(50) DEFAULT 'PENDING',
        requires_approval BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS dias_sessions (
        session_id VARCHAR(100) PRIMARY KEY,
        deal_id VARCHAR(100),
        status VARCHAR(50) DEFAULT 'ACTIVE',
        state_data JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS deal_documents (
        id SERIAL PRIMARY KEY,
        deal_id VARCHAR(100) REFERENCES deals(deal_id) ON DELETE CASCADE,
        doc_type VARCHAR(50) NOT NULL,
        title VARCHAR(255) NOT NULL,
        file_path TEXT,
        google_doc_url TEXT,
        google_sheet_url TEXT,
        drive_file_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    def __init__(self, db_url: Optional[str] = None):
        self.raw_url = db_url or os.getenv("NEON_DATABASE_URL")
        if not self.raw_url:
            self._load_fallback_env()
        self.connected = False
        self._schema_initialized = False
        self._in_memory_fallback: Dict[str, Any] = {
            "deals": {},
            "stakeholders": [],
            "interactions": [],
            "risks": [],
            "assessments": [],
            "actions": [],
            "sessions": {},
            "documents": []
        }
        self._init_db_connection()

    def _load_fallback_env(self) -> None:
        candidate_paths = [
            os.path.join(os.getcwd(), ".env"),
            os.path.expanduser("~/deal-intelligence-agent/.env"),
            os.path.expanduser("~/deal-intelligence-skill/.env"),
            os.path.expanduser("~/Documents/HACK WITH HYD/CODE/.env")
        ]
        for p in candidate_paths:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("NEON_DATABASE_URL="):
                                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                                if val:
                                    self.raw_url = val
                                    return
                except Exception:
                    pass

        if not self.raw_url:
            self.raw_url = "postgresql://neondb_owner:npg_DmBqkWziv0e4@ep-twilight-heart-b4629kfj-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"

    def _get_connection(self):
        """Creates a PostgreSQL connection, handling Neon SNI and IPv4 resolution."""
        if not PSYCOPG2_AVAILABLE or not self.raw_url:
            return None

        # Parse connection URL
        parsed = urllib.parse.urlparse(self.raw_url)
        hostname = parsed.hostname or ""
        endpoint_id = hostname.split(".")[0] if "." in hostname else ""

        # Resolve IPv4 to avoid Linux IPv6 blackhole timeout
        try:
            resolved_ip = socket.gethostbyname(hostname)
        except Exception:
            resolved_ip = hostname

        conn_params = {
            "host": resolved_ip,
            "port": parsed.port or 5432,
            "dbname": parsed.path.lstrip("/") or "neondb",
            "user": parsed.username or "neondb_owner",
            "password": parsed.password or "",
            "sslmode": "require",
            "connect_timeout": 10
        }

        # Neon requires the endpoint option when connecting directly by IP
        if endpoint_id:
            conn_params["options"] = f"endpoint={endpoint_id}"

        return psycopg2.connect(**conn_params)

    def _init_db_connection(self) -> bool:
        """Verifies database connectivity and provisions schema tables idempotently."""
        try:
            conn = self._get_connection()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    cur.execute(self.SCHEMA_DDL)
                    conn.commit()
                conn.close()
                self.connected = True
                self._schema_initialized = True
                logger.info("Successfully connected to Neon PostgreSQL and verified tables.")
                return True
        except Exception as e:
            logger.warning(f"Neon connection fallback active ({e})")
            self.connected = False
            return False

    def health_check(self) -> Tuple[bool, str, Dict[str, int]]:
        """Validates connection and returns table row counts."""
        if not self.connected:
            self._init_db_connection()

        if not self.connected:
            return False, "Neon PostgreSQL connection offline. Operating in resilient fallback mode.", {
                k: len(v) for k, v in self._in_memory_fallback.items()
            }

        counts = {}
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                for table in ["deals", "stakeholders", "deal_interactions", "deal_risks", "deal_assessments", "deal_actions", "dias_sessions", "deal_documents"]:
                    cur.execute(f"SELECT COUNT(*) FROM {table};")
                    counts[table] = cur.fetchone()[0]
            conn.close()
            return True, "Neon PostgreSQL operational and synchronized.", counts
        except Exception as e:
            return False, f"Neon health check error: {str(e)}", counts

    # 1. Deals CRUD
    def save_deal(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upserts a deal record."""
        deal_id = deal_data.get("deal_id", f"DEAL-{int(datetime.now().timestamp())}")
        customer = deal_data.get("customer", "Unknown Enterprise")
        owner = deal_data.get("owner", "Sales Lead")
        value = float(deal_data.get("value") or 0.0)
        currency = deal_data.get("currency", "USD")
        stage = deal_data.get("stage", "Discovery")
        budget_status = deal_data.get("budget_status", "Identified")
        competition = deal_data.get("competition") or deal_data.get("competitor", "None")
        timeline = deal_data.get("timeline", "Q4")
        verification_status = deal_data.get("verification_status", "verified")

        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO deals (deal_id, customer, owner, value, currency, stage, budget_status, competition, timeline, verification_status, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                        ON CONFLICT (deal_id) DO UPDATE SET
                            customer = EXCLUDED.customer,
                            owner = EXCLUDED.owner,
                            value = EXCLUDED.value,
                            currency = EXCLUDED.currency,
                            stage = EXCLUDED.stage,
                            budget_status = EXCLUDED.budget_status,
                            competition = EXCLUDED.competition,
                            timeline = EXCLUDED.timeline,
                            verification_status = EXCLUDED.verification_status,
                            updated_at = NOW();
                    """, (deal_id, customer, owner, value, currency, stage, budget_status, competition, timeline, verification_status))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save deal to Neon: {e}")

        # Local cache
        deal_record = {
            "deal_id": deal_id,
            "customer": customer,
            "owner": owner,
            "value": value,
            "currency": currency,
            "stage": stage,
            "budget_status": budget_status,
            "competition": competition,
            "timeline": timeline,
            "verification_status": verification_status,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self._in_memory_fallback["deals"][deal_id] = deal_record
        return deal_record

    def get_deal(self, deal_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a deal by ID."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM deals WHERE deal_id = %s;", (deal_id,))
                    row = cur.fetchone()
                conn.close()
                if row:
                    return dict(row)
            except Exception as e:
                logger.error(f"Failed to get deal from Neon: {e}")

        return self._in_memory_fallback["deals"].get(deal_id)

    # 2. Stakeholders CRUD
    def save_stakeholders(self, deal_id: str, stakeholders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Saves stakeholders associated with a deal."""
        saved = []
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    for s in stakeholders:
                        name = s.get("name", "Unknown")
                        role = s.get("role", "Stakeholder")
                        title = s.get("title", "")
                        email = s.get("email", "")
                        auth = s.get("buying_authority", "Influencer")
                        sentiment = s.get("sentiment", "Neutral")
                        cur.execute("""
                            INSERT INTO stakeholders (deal_id, name, role, title, email, buying_authority, sentiment)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """, (deal_id, name, role, title, email, auth, sentiment))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save stakeholders to Neon: {e}")

        for s in stakeholders:
            entry = dict(s)
            entry["deal_id"] = deal_id
            self._in_memory_fallback["stakeholders"].append(entry)
            saved.append(entry)
        return saved

    def get_stakeholders(self, deal_id: str) -> List[Dict[str, Any]]:
        """Retrieves stakeholders for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM stakeholders WHERE deal_id = %s;", (deal_id,))
                    rows = cur.fetchall()
                conn.close()
                if rows:
                    return [dict(r) for r in rows]
            except Exception as e:
                logger.error(f"Failed to get stakeholders from Neon: {e}")

        return [s for s in self._in_memory_fallback["stakeholders"] if s.get("deal_id") == deal_id]

    # 3. Interactions CRUD
    def record_interaction(self, deal_id: str, event_type: str, content: str, source: str = "user_input") -> Dict[str, Any]:
        """Records a deal interaction / meeting note."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO deal_interactions (deal_id, event_type, content, source)
                        VALUES (%s, %s, %s, %s);
                    """, (deal_id, event_type, content, source))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to record interaction in Neon: {e}")

        rec = {
            "deal_id": deal_id,
            "event_type": event_type,
            "content": content,
            "source": source,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self._in_memory_fallback["interactions"].append(rec)
        return rec

    def get_interactions(self, deal_id: str) -> List[Dict[str, Any]]:
        """Retrieves interactions for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM deal_interactions WHERE deal_id = %s ORDER BY created_at DESC;", (deal_id,))
                    rows = cur.fetchall()
                conn.close()
                if rows:
                    return [dict(r) for r in rows]
            except Exception as e:
                logger.error(f"Failed to get interactions from Neon: {e}")

        return [i for i in self._in_memory_fallback["interactions"] if i.get("deal_id") == deal_id]

    # 4. Risks & Mitigations
    def save_risks(self, deal_id: str, risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Saves risks and mitigations for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    for r in risks:
                        cur.execute("""
                            INSERT INTO deal_risks (deal_id, risk_type, description, severity, mitigation, status)
                            VALUES (%s, %s, %s, %s, %s, %s);
                        """, (
                            deal_id,
                            r.get("risk_type", "General"),
                            r.get("description", ""),
                            r.get("severity", "Medium"),
                            r.get("mitigation", ""),
                            r.get("status", "Identified")
                        ))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save risks in Neon: {e}")

        for r in risks:
            entry = dict(r)
            entry["deal_id"] = deal_id
            self._in_memory_fallback["risks"].append(entry)
        return risks

    def get_risks(self, deal_id: str) -> List[Dict[str, Any]]:
        """Retrieves risks for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM deal_risks WHERE deal_id = %s;", (deal_id,))
                    rows = cur.fetchall()
                conn.close()
                if rows:
                    return [dict(r) for r in rows]
            except Exception as e:
                logger.error(f"Failed to get risks from Neon: {e}")

        return [r for r in self._in_memory_fallback["risks"] if r.get("deal_id") == deal_id]

    # 5. Assessments
    def save_assessment(self, deal_id: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a multi-vector health score and breakdown."""
        health = float(assessment_data.get("health_score", 0.0))
        win_prob = float(assessment_data.get("win_probability", 0.0))
        breakdown = json.dumps(assessment_data.get("breakdown", {}))
        version = assessment_data.get("model_version", "1.0.0")

        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO deal_assessments (deal_id, overall_health, win_probability, scoring_breakdown, model_version)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (deal_id, health, win_prob, breakdown, version))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save assessment in Neon: {e}")

        rec = {
            "deal_id": deal_id,
            "overall_health": health,
            "win_probability": win_prob,
            "scoring_breakdown": assessment_data.get("breakdown", {}),
            "model_version": version,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self._in_memory_fallback["assessments"].append(rec)
        return rec

    def get_latest_assessment(self, deal_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the latest assessment for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("""
                        SELECT * FROM deal_assessments WHERE deal_id = %s
                        ORDER BY created_at DESC LIMIT 1;
                    """, (deal_id,))
                    row = cur.fetchone()
                conn.close()
                if row:
                    return dict(row)
            except Exception as e:
                logger.error(f"Failed to get assessment from Neon: {e}")

        matched = [a for a in self._in_memory_fallback["assessments"] if a.get("deal_id") == deal_id]
        return matched[-1] if matched else None

    # 6. Action Items
    def save_actions(self, deal_id: str, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Saves action items / next steps."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    for a in actions:
                        cur.execute("""
                            INSERT INTO deal_actions (deal_id, action_type, title, description, owner, due_date, status, requires_approval)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """, (
                            deal_id,
                            a.get("action_type", "task"),
                            a.get("title", "Action"),
                            a.get("description", ""),
                            a.get("owner", "AE"),
                            a.get("due_date", ""),
                            a.get("status", "PENDING"),
                            a.get("requires_approval", True)
                        ))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save actions in Neon: {e}")

        for a in actions:
            entry = dict(a)
            entry["deal_id"] = deal_id
            self._in_memory_fallback["actions"].append(entry)
        return actions

    def get_actions(self, deal_id: str) -> List[Dict[str, Any]]:
        """Retrieves action items for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM deal_actions WHERE deal_id = %s;", (deal_id,))
                    rows = cur.fetchall()
                conn.close()
                if rows:
                    return [dict(r) for r in rows]
            except Exception as e:
                logger.error(f"Failed to get actions from Neon: {e}")

        return [a for a in self._in_memory_fallback["actions"] if a.get("deal_id") == deal_id]

    # 7. Session State Persistence
    def save_session(self, session_id: str, deal_id: Optional[str], status: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves or updates multi-turn DIAS session state."""
        state_json = json.dumps(state_data)
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO dias_sessions (session_id, deal_id, status, state_data, updated_at)
                        VALUES (%s, %s, %s, %s, NOW())
                        ON CONFLICT (session_id) DO UPDATE SET
                            deal_id = EXCLUDED.deal_id,
                            status = EXCLUDED.status,
                            state_data = EXCLUDED.state_data,
                            updated_at = NOW();
                    """, (session_id, deal_id, status, state_json))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save session in Neon: {e}")

        entry = {
            "session_id": session_id,
            "deal_id": deal_id,
            "status": status,
            "state_data": state_data,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self._in_memory_fallback["sessions"][session_id] = entry
        return entry

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a session by ID."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM dias_sessions WHERE session_id = %s;", (session_id,))
                    row = cur.fetchone()
                conn.close()
                if row:
                    return dict(row)
            except Exception as e:
                logger.error(f"Failed to get session from Neon: {e}")

        return self._in_memory_fallback["sessions"].get(session_id)

    # 8. Generated Document References
    def save_document(
        self,
        deal_id: str,
        doc_type: str,
        title: str,
        file_path: Optional[str] = None,
        google_doc_url: Optional[str] = None,
        google_sheet_url: Optional[str] = None,
        drive_file_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Stores reference to generated executive deliverables."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO deal_documents (deal_id, doc_type, title, file_path, google_doc_url, google_sheet_url, drive_file_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (deal_id, doc_type, title, file_path, google_doc_url, google_sheet_url, drive_file_id))
                    conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to save document reference in Neon: {e}")

        rec = {
            "deal_id": deal_id,
            "doc_type": doc_type,
            "title": title,
            "file_path": file_path,
            "google_doc_url": google_doc_url,
            "google_sheet_url": google_sheet_url,
            "drive_file_id": drive_file_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self._in_memory_fallback["documents"].append(rec)
        return rec

    def get_documents(self, deal_id: str) -> List[Dict[str, Any]]:
        """Retrieves all documents for a deal."""
        if self.connected:
            try:
                conn = self._get_connection()
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM deal_documents WHERE deal_id = %s;", (deal_id,))
                    rows = cur.fetchall()
                conn.close()
                if rows:
                    return [dict(r) for r in rows]
            except Exception as e:
                logger.error(f"Failed to get documents from Neon: {e}")

        return [d for d in self._in_memory_fallback["documents"] if d.get("deal_id") == deal_id]
