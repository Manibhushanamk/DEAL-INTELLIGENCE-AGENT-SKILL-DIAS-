from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class FactExtraction(BaseModel):
    fact: str
    category: str
    confidence: float = 1.0
    source_interaction_id: str

class DealFact(BaseModel):
    deal_id: str
    customer: str
    event_type: str = "interaction"
    content: str
    stakeholders: List[str] = Field(default_factory=list)
    competitors: List[str] = Field(default_factory=list)
    budget: Optional[str] = None
    timeline: Optional[str] = None
    objections: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TelemetryEvent(BaseModel):
    event_id: str
    session_id: str
    query_intent: str
    tool_invoked: Optional[str] = None
    friction_detected: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class MemoryRetainRequest(BaseModel):
    namespace: str = "dias_deals"
    key: str
    data: Dict[str, Any]
    retention_policy: str = "persistent"
    memory_bank_id: Optional[str] = None

class MemoryRecallRequest(BaseModel):
    namespace: str = "dias_deals"
    query: str
    top_k: int = 5
    memory_bank_id: Optional[str] = None

class MemoryReflectRequest(BaseModel):
    namespace: str = "dias_deals"
    topic: str = "deal_strategy"
    memory_bank_id: Optional[str] = None
