from fastapi import APIRouter, HTTPException, status
from models.schemas import ReviewRequest, ReviewResponse
from services import github, analyzer, llm_reviewer

router = APIRouter(prefix="/api/v1", tags=["Code Review"])

@router.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    """
    Analyzes and reviews code from a GitHub URL or a raw diff string.

    - **github_url**: URL of the GitHub repository to analyze.
    - **diff_content**: A raw string of a git diff to analyze.

    One of the two fields must be provided.
    """
    code_to_review = ""
    
    if request.diff_content:
        code_to_review = request.diff_content
    elif request.github_url:
        code_to_review = await github.get_code_from_github(request.github_url)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'github_url' or 'diff_content' must be provided."
        )

    if not code_to_review.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided source is empty."
        )

    # 1. Perform initial static analysis (dummy)
    static_analysis_results = analyzer.perform_static_analysis(code_to_review)

    # 2. Get comprehensive review from LLM, using static analysis as context
    final_review = await llm_reviewer.get_llm_review(code_to_review, static_analysis_results)
    
    return final_review