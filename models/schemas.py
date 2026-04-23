# ARK_MEMORY_SYSTEM_ACTIVE
from pydantic import BaseModel

class StaticAuditRequest(BaseModel):
    """
    Request model for static analysis audit.
    """
    target_path: str