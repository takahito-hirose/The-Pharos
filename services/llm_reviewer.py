import litellm
import os
from fastapi import HTTPException, status
from models.schemas import ReviewResponse, CategoryScore
from core.config import settings
from typing import Dict

# Set API key for litellm. It automatically detects the provider from the model name.
# For example, for "gpt-4o", it will look for OPENAI_API_KEY.
os.environ["OPENAI_API_KEY"] = settings.LLM_API_KEY
# Add keys for other providers if you use them, e.g.:
# os.environ["GEMINI_API_KEY"] = settings.LLM_API_KEY

async def get_llm_review(code: str, static_analysis_results: Dict[str, CategoryScore]) -> ReviewResponse:
    """
    Uses an LLM to review the given code, taking initial static analysis results as context,
    and returns a structured response.
    """
    system_prompt = """
    You are an expert code reviewer. You will be given a piece of code and the results from a preliminary static analysis tool.
    Your task is to perform a comprehensive review, building upon the static analysis findings.
    Analyze the code for security, maintainability, and performance.
    - Validate, refine, or add to the issues found by the static analysis.
    - Provide a final score from 0 to 100 for each category (100 being the best).
    - For each category, list the final set of identified issues and provide actionable suggestions for improvement.
    - Write a brief overall summary of the code quality.
    Your response MUST be in the format of the provided JSON schema. Do not just repeat the static analysis input; use your own expertise to create a complete review.
    """

    user_prompt = f"""
    Please review the following code.

    --- CODE ---
    {code}
    ---

    --- PRELIMINARY STATIC ANALYSIS RESULTS ---
    Security: {static_analysis_results['security'].model_dump_json(indent=2)}
    Maintainability: {static_analysis_results['maintainability'].model_dump_json(indent=2)}
    Performance: {static_analysis_results['performance'].model_dump_json(indent=2)}
    ---

    Now, provide your final, comprehensive review in the required JSON format.
    """

    try:
        # Using litellm's structured output feature with Pydantic
        response = await litellm.acompletion(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_model=ReviewResponse,
        )
        # The response object is already a Pydantic model instance
        return response
    except Exception as e:
        # Catch specific litellm exceptions if possible, e.g., litellm.exceptions.APIError
        print(f"LLM review failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during the LLM review: {e}",
        )