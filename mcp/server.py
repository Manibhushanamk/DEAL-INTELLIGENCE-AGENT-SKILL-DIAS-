import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
logger = logging.getLogger("DIAS_MCPServer")
logger.setLevel(logging.INFO)

class MCPServer:
    """
    Model Context Protocol (MCP) server for Deal Intelligence Agent Skill (DIAS).
    Exposes cognitive memory tools, deal analytics, dossier compilation,
    workspace staging, and adaptive recommendations over standard JSON-RPC 2.0 stdio.
    """
    def __init__(self, skill: Optional[Any] = None):
        if skill is None:
            from src.core_skill import DealIntelligenceSkill
            self.skill = DealIntelligenceSkill()
        else:
            self.skill = skill
        self.tools_schema = self._load_schema()

    def _load_schema(self) -> List[Dict[str, Any]]:
        schema_path = os.path.join(os.path.dirname(__file__), "tools.json")
        if os.path.exists(schema_path):
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read tools.json: {e}")
        return []

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns the list of available MCP tool definitions."""
        return self.tools_schema

    def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches an MCP tool call to the corresponding skill method."""
        logger.info(f"[MCP Server] Executing tool: '{tool_name}'")
        try:
            if tool_name == "memory_retain":
                res = self.skill.memory_retain(
                    namespace=arguments.get("namespace", "dias_deals"),
                    key=arguments.get("key", "default_key"),
                    data=arguments.get("data", {}),
                )
                return {"status": "success", "result": res}

            elif tool_name == "memory_recall":
                res = self.skill.memory_recall(
                    namespace=arguments.get("namespace", "dias_deals"),
                    query=arguments.get("query", ""),
                    top_k=arguments.get("top_k", 5)
                )
                return {"status": "success", "result": res}

            elif tool_name == "memory_reflect":
                res = self.skill.memory_reflect(
                    namespace=arguments.get("namespace", "dias_deals"),
                    topic=arguments.get("topic", "deal_strategy")
                )
                return {"status": "success", "result": res}

            elif tool_name == "deal_analytics":
                res = self.skill.deal_analytics(
                    deal_data=arguments.get("deal_data", {})
                )
                return {"status": "success", "result": res}

            elif tool_name == "generate_dossier":
                path = self.skill.generate_dossier(
                    output_filepath=arguments.get("output_filepath", "dossier.pdf"),
                    account_name=arguments.get("account_name", "Enterprise Account"),
                    deal_data=arguments.get("deal_data", {})
                )
                return {"status": "success", "result": {"pdf_path": path}}

            elif tool_name == "stage_workspace":
                res = self.skill.stage_workspace(
                    action_type=arguments.get("action_type", "email"),
                    params=arguments.get("params", {})
                )
                return {"status": "success", "result": res}

            elif tool_name == "get_adaptive_recommendations":
                recs = self.skill.get_adaptive_recommendations()
                return {"status": "success", "result": recs}

            elif tool_name == "connect_mcp":
                res = self.skill.connect_mcp(
                    mcp_id=arguments.get("mcp_id", ""),
                    config=arguments.get("config", {})
                )
                return {"status": "success", "result": res}

            else:
                return {"status": "error", "error": f"Unknown tool: '{tool_name}'"}

        except Exception as e:
            logger.error(f"[MCP Server] Error executing '{tool_name}': {e}")
            return {"status": "error", "error": str(e)}

    def run_stdio(self) -> None:
        """
        Runs the standard MCP JSON-RPC 2.0 stdio server loop for host agents.
        """
        logger.info("[MCP Server] Starting DIAS stdio transport loop.")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                req_id = req.get("id")
                method = req.get("method")
                params = req.get("params", {})

                if method == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"tools": self.list_tools()}
                    }
                elif method == "tools/call":
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    out = self.handle_tool_call(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": out
                    }
                elif method == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {}},
                            "serverInfo": {"name": "deal-intelligence-skill", "version": "1.0.0"}
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Method not found: {method}"}
                    }

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()

def main():
    server = MCPServer()
    server.run_stdio()

if __name__ == "__main__":
    main()
