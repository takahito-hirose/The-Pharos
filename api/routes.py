from fastapi import APIRouter, HTTPException, status
from models.schemas import ReviewRequest, ReviewResponse, CategoryScore

router = APIRouter()

@router.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    """
    Accepts a GitHub URL or a git diff and returns a dummy code review analysis.
    """
    if not request.github_url and not request.diff_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'github_url' or 'diff_content' must be provided."
        )

    # This is a dummy response. In the future, this will be replaced by
    # calls to the services for static analysis and LLM review.
    dummy_security = CategoryScore(
        score=85,
        issues=["Found one potential SQL injection vulnerability."],
        suggestions=["Use parameterized queries to prevent SQL injection."]
    )
    dummy_maintainability = CategoryScore(
        score=70,
        issues=["Function 'calculate_total' is too long (over 50 lines).", "Lack of comments in complex logic."],
        suggestions=["Refactor 'calculate_total' into smaller, single-responsibility functions.", "Add comments to explain the business logic."]
    )
    dummy_performance = CategoryScore(
        score=92,
        issues=["Inefficient loop in data processing module."],
        suggestions=["Consider using a more efficient algorithm or data structure."]
    )

    return ReviewResponse(
        security=dummy_security,
        maintainability=dummy_maintainability,
        performance=dummy_performance,
        overall_summary="The code is generally well-structured but has some areas for improvement in maintainability and security."
    )