# ARK_MEMORY_SYSTEM_ACTIVE
import json
import re
import subprocess
from pathlib import Path

import litellm
from fastapi import APIRouter, HTTPException
from models.schemas import (
    ReviewRequest,
    ReviewResponse,
    StaticAuditRequest,
    StaticAuditResponse,
)
from core.config import settings

router = APIRouter()


# ---------------------------------------------------------------------------
# First defense line: static analysis via flake8
# ---------------------------------------------------------------------------

@router.post("/audit/static", response_model=StaticAuditResponse)
async def run_static_audit(request: StaticAuditRequest):
    """
    Runs a static analysis on the given target path using flake8.
    First defense line of The Pharos API.
    """
    target = Path(request.target_path)

    if not target.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Target path not found: {request.target_path}",
        )

    result = subprocess.run(
        ["flake8", str(target)],
        capture_output=True,
        text=True,
    )

    issues = [line for line in result.stdout.splitlines() if line.strip()]

    score = max(0, 100 - len(issues) * 5)

    return StaticAuditResponse(
        status="success",
        score=score,
        message=f"Static analysis completed for: {request.target_path}",
        issues=issues,
    )


# ---------------------------------------------------------------------------
# Second defense line: AI Scoring Engine via LLM (Pentagram – 5 axes)
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are an expert code reviewer. Analyse the provided code and respond ONLY
with a single JSON object that matches this exact schema — no markdown fences,
no extra keys:

{
  "security": {
    "score": <int 0-100>,
    "issues": [<string>, ...],
    "suggestions": [<string>, ...]
  },
  "performance": {
    "score": <int 0-100>,
    "issues": [<string>, ...],
    "suggestions": [<string>, ...]
  },
  "maintainability": {
    "score": <int 0-100>,
    "issues": [<string>, ...],
    "suggestions": [<string>, ...]
  },
  "resilience": {
    "score": <int 0-100>,
    "issues": [<string>, ...],
    "suggestions": [<string>, ...]
  },
  "testability": {
    "score": <int 0-100>,
    "issues": [<string>, ...],
    "suggestions": [<string>, ...]
  },
  "overall_summary": "<one-paragraph summary>"
}
"""

# Pattern to extract the outermost JSON object from LLM output that may
# contain markdown fences (```json ... ```) or surrounding prose.
_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(raw: str) -> str:
    """Return the first top-level JSON object found in *raw*.

    Local LLMs (e.g. Ollama/Gemma) often wrap their JSON in markdown code
    fences or add explanatory text.  This helper strips everything outside
    the outermost ``{ … }`` pair so that ``json.loads`` can succeed.
    """
    match = _JSON_OBJECT_RE.search(raw)
    if match is None:
        return raw  # fall through – let json.loads raise a clear error
    return match.group(0)


@router.post("/audit/ai", response_model=ReviewResponse)
async def run_ai_audit(request: ReviewRequest):
    """
    Runs an AI-powered code review using an LLM via litellm.
    Second defense line of The Pharos API.
    """
    target = Path(request.target_path)

    if not target.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Target path not found: {request.target_path}",
        )

    code_content = target.read_text(encoding="utf-8")

    user_message = f"Review the following code:\n\n```\n{code_content}\n```"
    if request.context:
        user_message = f"Context: {request.context}\n\n{user_message}"

    try:
        llm_response = await litellm.acompletion(
            model=settings.REVIEW_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM call failed: {exc}",
        )

    raw_content = llm_response.choices[0].message.content

    try:
        cleaned = _extract_json(raw_content)
        parsed = json.loads(cleaned)
        review = ReviewResponse(**parsed)
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to parse LLM response: {exc}. Raw: {raw_content[:200]}",
        )

    return review