# ARK_MEMORY_SYSTEM_ACTIVE
from pydantic import BaseModel, Field


class StaticAuditRequest(BaseModel):
    """
    Request model for static analysis audit.
    """
    target_path: str


class StaticAuditResponse(BaseModel):
    """
    Response model for static analysis audit.
    """
    status: str
    score: int
    message: str
    issues: list[str] = Field(default_factory=list)