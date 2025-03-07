from typing import Dict, Any
from models.schemas import WorkflowRequest

class PayloadGenerator:
    @staticmethod
    def generate_payload(workflow: WorkflowRequest) -> Dict[str, Any]:
        payload = {}
        placeholder = "placeholder"
        
        for node in workflow.nodes:
            for tool in node.tools_to_use:
                for param in tool.tool_params.items:
                    if param.user_dependent:
                        payload[param.field_name] = placeholder
        return payload