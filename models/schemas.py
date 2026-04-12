from pydantic import BaseModel, Field
from typing import List, Optional

class ReviewRequest(BaseModel):
    github_url: Optional[str] = Field(None, description="GitHub Repository URL")
    diff_content: Optional[str] = Field(None, description="Raw Git Diff string")

class CategoryScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Score out of 100")
    issues: List[str] = Field(..., description="List of identified issues")
    suggestions: List[str] = Field(..., description="Actionable improvement suggestions")

class ReviewResponse(BaseModel):
    security: CategoryScore
    maintainability: CategoryScore
    performance: CategoryScore
    overall_summary: str = Field(..., description="Brief overall evaluation summary")