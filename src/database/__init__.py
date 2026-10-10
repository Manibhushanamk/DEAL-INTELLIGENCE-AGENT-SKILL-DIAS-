"""
Neon PostgreSQL Database Module for DIAS.
Authoritative source for structured deal records, stakeholder maps,
assessments, milestones, risks, actions, and session states.
"""
from src.database.neon_client import NeonClient

__all__ = ["NeonClient"]
