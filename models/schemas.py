from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ToolParamItem(BaseModel):
    field_name: str
    user_dependent: bool

class ToolParams(BaseModel):
    items: List[ToolParamItem]

class ToolToUse(BaseModel):
    tool_id: int
    tool_name: str
    tool_params: ToolParams

class Node(BaseModel):
    node_id: str
    tools_to_use: List[ToolToUse]

class Connection(BaseModel):
    from_node: str
    to: str
    conditional_routing: str

class WorkflowRequest(BaseModel):
    nodes: List[Node]
    connections: List[Connection]

class CodeRequest(BaseModel):
    workflow: WorkflowRequest
    language: str
    base_url: Optional[str] = "https://forty-needles-draw.loca.lt"

class PayloadResponse(BaseModel):
    payload: Dict[str, Any]

class CodeResponse(BaseModel):
    code: str
    payload: Dict[str, Any]