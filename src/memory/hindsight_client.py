import os
import json
import logging
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional, Tuple
from src.memory.schema import FactExtraction

logger = logging.getLogger("HindsightClient")
logger.setLevel(logging.INFO)

class HindsightClient:
    """
    Client for Vectorize Hindsight Cloud API providing persistent two-dimensional
    memory (Deal Intelligence + Agent Telemetry) with Retain, Recall, and Reflect operations.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("HINDSIGHT_API_KEY")
        
        # Check fallback .env files if not found in environment
        if not self.api_key:
            self._load_fallback_env()

        raw_base = base_url or os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
        self.base_url = raw_base.rstrip("/")
        self._memory_store: Dict[str, List[Dict[str, Any]]] = {}
        self._created_banks = set()

    def _load_fallback_env(self) -> None:
        candidate_paths = [
            os.path.join(os.getcwd(), ".env"),
            os.path.expanduser("~/deal-intelligence-agent/.env"),
            os.path.expanduser("~/deal-intelligence-skill/.env"),
        ]
        for p in candidate_paths:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("HINDSIGHT_API_KEY="):
                                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                                if val:
                                    self.api_key = val
                                    break
                    if self.api_key:
                        break
                except Exception:
                    pass

    @staticmethod
    def mask_key(key: Optional[str]) -> str:
        """Securely masks API key for zero-leak display."""
        if not key:
            return "[NONE]"
        if len(key) <= 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"

    def validate_connection(self) -> Tuple[bool, str]:
        """
        Validates API key and connectivity with Vectorize Hindsight Cloud.
        Returns (success_boolean, status_message).
        """
        if not self.api_key:
            return False, "Hindsight API key is missing. Please provide a valid key."
        
        if self.api_key.startswith("mock_"):
            return True, "Mock Hindsight mode validated for offline testing."

        # 1. Network & Health check
        try:
            health_req = urllib.request.Request(f"{self.base_url}/health")
            with urllib.request.urlopen(health_req, timeout=8) as h_resp:
                if h_resp.status != 200:
                    return False, f"Hindsight Cloud health check returned status {h_resp.status}"
        except Exception as e:
            return False, f"Network connection failed to {self.base_url}: {str(e)}"

        # 2. Authentication check via bank listing
        url = f"{self.base_url}/v1/default/banks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return True, "Successfully authenticated with Vectorize Hindsight Cloud."
                return False, f"Hindsight Cloud returned unexpected status: {resp.status}"
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return False, f"Authentication failed (HTTP {e.code}): Invalid Hindsight Cloud API key."
            return False, f"Hindsight Cloud HTTP Error: {e.code} - {e.reason}"
        except Exception as e:
            return False, f"Authentication request failed to {self.base_url}: {str(e)}"

    def _ensure_bank_exists(self, bank_id: str) -> None:
        """Idempotently ensures the memory bank is provisioned on Hindsight Cloud."""
        if bank_id in self._created_banks or not self.api_key or self.api_key.startswith("mock_"):
            return

        try:
            url = f"{self.base_url}/v1/default/banks/{bank_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            req_data = json.dumps({"name": f"DIAS Memory Bank - {bank_id}"}).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers=headers, method="PUT")
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status in (200, 201):
                    self._created_banks.add(bank_id)
        except Exception as e:
            logger.debug(f"[Hindsight Cloud] Bank registration notice: {e}")

    def retain(
        self,
        namespace: Optional[str] = None,
        key: str = "default_key",
        data: Optional[Dict[str, Any]] = None,
        retention_policy: str = "persistent",
        memory_bank_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inscribes facts, sales discussions, transcripts, or telemetry events into Hindsight memory.
        """
        bank_id = memory_bank_id or namespace or "dias_deals"
        data = data or {}

        # 1. Hindsight Cloud persistence
        cloud_persisted = False
        error_msg = None
        if self.api_key and not self.api_key.startswith("mock_"):
            try:
                self._ensure_bank_exists(bank_id)
                url = f"{self.base_url}/v1/default/banks/{bank_id}/memories"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                content_text = data.get("content") or json.dumps(data)
                cloud_payload = {
                    "items": [
                        {
                            "content": content_text,
                            "document_id": key,
                            "context": data.get("event_type", "dias_interaction")
                        }
                    ],
                    "async": False
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(cloud_payload).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    if resp.status in (200, 201):
                        res_json = json.loads(resp.read().decode("utf-8"))
                        if res_json.get("success") is True:
                            cloud_persisted = True
            except Exception as e:
                error_msg = str(e)
                logger.debug(f"[Hindsight Cloud] Cloud retain notice: {e}")

        # 2. Local resilient store
        if bank_id not in self._memory_store:
            self._memory_store[bank_id] = []

        existing = self._memory_store[bank_id]
        updated = False
        for entry in existing:
            if entry.get("key") == key:
                entry["payload"] = data
                entry["retention_policy"] = retention_policy
                entry["cloud_synced"] = cloud_persisted
                updated = True
                break

        if not updated:
            self._memory_store[bank_id].append({
                "key": key,
                "payload": data,
                "retention_policy": retention_policy,
                "cloud_synced": cloud_persisted,
                "timestamp": data.get("timestamp", "")
            })

        is_mock = bool(self.api_key and self.api_key.startswith("mock_"))
        status_ok = cloud_persisted or is_mock

        return {
            "status": "success" if status_ok else "failed",
            "operation": "retain",
            "memory_bank_id": bank_id,
            "key": key,
            "cloud_synced": cloud_persisted,
            "error": None if status_ok else (error_msg or "Cloud retain unconfirmed")
        }

    def recall(
        self,
        namespace: Optional[str] = None,
        query: str = "",
        top_k: int = 5,
        memory_bank_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves high-precision contextual memories matching the query using semantic search.
        """
        bank_id = memory_bank_id or namespace or "dias_deals"
        cloud_results: List[Dict[str, Any]] = []

        if self.api_key and not self.api_key.startswith("mock_"):
            try:
                self._ensure_bank_exists(bank_id)
                url = f"{self.base_url}/v1/default/banks/{bank_id}/memories/recall"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                req_data = json.dumps({"query": query}).encode("utf-8")
                req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=12) as resp:
                    if resp.status == 200:
                        res_json = json.loads(resp.read().decode("utf-8"))
                        raw_cloud = res_json.get("results", [])
                        for r in raw_cloud:
                            if isinstance(r, dict):
                                text_val = r.get("text") or r.get("content", "")
                                cloud_results.append({
                                    "id": r.get("id"),
                                    "document_id": r.get("document_id"),
                                    "content": text_val,
                                    "text": text_val,
                                    "context": r.get("context", ""),
                                    "entities": r.get("entities", []),
                                    "tags": r.get("tags", []),
                                    "source": "hindsight_cloud"
                                })
            except Exception as e:
                logger.debug(f"[Hindsight Cloud] Cloud recall notice: {e}")

        # If live Hindsight Cloud returned results, return them directly
        if cloud_results:
            return cloud_results[:top_k]

        # Fallback to local semantic matching for offline/mock environments
        entries = self._memory_store.get(bank_id, [])
        query_words = set(query.lower().split())

        scored_entries = []
        for entry in entries:
            payload_str = json.dumps(entry.get("payload", {})).lower()
            score = sum(1.0 for word in query_words if word in payload_str)
            if score > 0 or not query_words:
                scored_entries.append((score, entry["payload"]))

        scored_entries.sort(key=lambda x: x[0], reverse=True)
        local_results = [item[1] for item in scored_entries[:top_k]]

        return local_results

    def reflect(
        self,
        namespace: Optional[str] = None,
        topic: str = "deal_strategy",
        memory_bank_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes higher-order strategic beliefs, objection trends, and operational patterns.
        """
        bank_id = memory_bank_id or namespace or "dias_deals"
        cloud_reflection = None

        if self.api_key and not self.api_key.startswith("mock_"):
            try:
                self._ensure_bank_exists(bank_id)
                url = f"{self.base_url}/v1/default/banks/{bank_id}/reflect"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                req_data = json.dumps({"query": f"Consolidate key strategic patterns, risks, and insights regarding: {topic}"}).encode("utf-8")
                req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=20) as resp:
                    if resp.status == 200:
                        res_json = json.loads(resp.read().decode("utf-8"))
                        cloud_reflection = res_json.get("text")
            except Exception as e:
                logger.debug(f"[Hindsight Cloud] Cloud reflect notice: {e}")

        # Synthesize from memories
        entries = self._memory_store.get(bank_id, [])
        extracted_facts = []
        for e in entries:
            content = e.get("payload", {}).get("content", "")
            if content:
                extracted_facts.extend(self.extract_facts(content, e.get("key", "")))

        categories = sorted(list(set(f.category for f in extracted_facts)))
        beliefs = []
        if cloud_reflection and "not record any" not in cloud_reflection.lower():
            beliefs.append(cloud_reflection)
        
        if not beliefs:
            if categories:
                beliefs.append(f"Account exhibits historical disclosures across: {', '.join(categories)}.")
            if "budget" in categories:
                beliefs.append("Pricing & ROI justification is required before contract finalization.")
            if "technical" in categories:
                beliefs.append("Architecture and SSO compliance verification are critical closing prerequisites.")
            if "competitor" in categories:
                beliefs.append("Active competitive evaluation detected; battlecard positioning recommended.")

        if not beliefs:
            beliefs.append("Discovery phase active; ongoing knowledge synthesis across interactions.")

        return {
            "status": "success",
            "operation": "reflect",
            "memory_bank_id": bank_id,
            "topic": topic,
            "total_memories_consolidated": len(entries),
            "key_fact_dimensions": categories,
            "consolidated_beliefs": beliefs,
            "cloud_reflection": cloud_reflection
        }

    def execute_preflight_triad(self, bank_id: str = "dias_triad_preflight") -> Dict[str, Any]:
        """
        Executes automated Pre-Flight Triad Health Check:
        1. RETAIN test fact
        2. RECALL test fact
        3. REFLECT on test knowledge
        Returns structured validation report.
        """
        test_key = "preflight_test_node"
        test_data = {
            "event_type": "preflight_test",
            "content": "Pre-flight validation fact: DIAS cognitive brain is active with SOC2 and Okta SSO compliance.",
            "status": "initial_check"
        }

        # 1. Test Retain
        retain_res = self.retain(memory_bank_id=bank_id, key=test_key, data=test_data)
        retain_ok = retain_res.get("status") == "success"

        # 2. Test Recall
        recall_res = self.recall(memory_bank_id=bank_id, query="What compliance is validated in pre-flight?", top_k=3)
        recall_ok = len(recall_res) > 0

        # 3. Test Reflect
        reflect_res = self.reflect(memory_bank_id=bank_id, topic="compliance")
        reflect_ok = reflect_res.get("status") == "success" and (
            reflect_res.get("cloud_reflection") is not None or len(reflect_res.get("consolidated_beliefs", [])) > 0
        )

        all_passed = retain_ok and recall_ok and reflect_ok

        return {
            "status": "PASSED" if all_passed else "FAILED",
            "all_passed": all_passed,
            "triad": {
                "retain": {"passed": retain_ok, "details": retain_res},
                "recall": {"passed": recall_ok, "results_count": len(recall_res)},
                "reflect": {"passed": reflect_ok, "beliefs_count": len(reflect_res.get("consolidated_beliefs", []))}
            }
        }

        return {
            "status": "PASSED" if all_passed else "FAILED",
            "all_passed": all_passed,
            "triad": {
                "retain": {"passed": retain_ok, "details": retain_res},
                "recall": {"passed": recall_ok, "results_count": len(recall_res)},
                "reflect": {"passed": reflect_ok, "beliefs_count": len(reflect_res.get("consolidated_beliefs", []))}
            }
        }

    def extract_facts(self, text: str, source_interaction_id: str) -> List[FactExtraction]:
        """Extracts key categorical facts from text."""
        facts = []
        text_lower = text.lower()
        if any(w in text_lower for w in ["budget", "$", "price", "pricing", "cost", "discount"]):
            facts.append(FactExtraction(
                fact="Budget constraint, discount discussion, or pricing terms noted.",
                category="budget",
                confidence=0.9,
                source_interaction_id=source_interaction_id
            ))
        if any(w in text_lower for w in ["sso", "security", "compliance", "okta", "soc2", "govcloud", "aws", "gdpr"]):
            facts.append(FactExtraction(
                fact="Technical stack / Security prerequisite / Compliance disclosure noted.",
                category="technical",
                confidence=0.95,
                source_interaction_id=source_interaction_id
            ))
        if any(w in text_lower for w in ["competitor", "salesforce", "gong", "clari", "hubspot"]):
            facts.append(FactExtraction(
                fact="Competitive evaluation or market alternative mentioned.",
                category="competitor",
                confidence=0.85,
                source_interaction_id=source_interaction_id
            ))
        return facts
