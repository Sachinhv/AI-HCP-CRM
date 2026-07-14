from typing import TypedDict, Optional, Dict, Any


class CRMState(TypedDict):
    user_input: str
    tool: Optional[str]
    result: Dict[str, Any]