# ARK_MEMORY_SYSTEM_ACTIVE
from typing import Optional
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


# --- AI Scoring Engine schemas ---

class ReviewRequest(BaseModel):
    """
    Request model for AI code review.
    """
    target_path: str
    context: Optional[str] = None


class CategoryScore(BaseModel):
    """
    Score and findings for a single review category.
    """
    score: int
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class ReviewResponse(BaseModel):
    """
    Full AI review result broken down by category.
    """
    security: CategoryScore
    performance: CategoryScore
    maintainability: CategoryScore
    overall_summary: str