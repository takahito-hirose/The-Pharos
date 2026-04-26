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
# 🌟 The Pharos Brain: Load Prompt from External Markdown
# ---------------------------------------------------------------------------
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "reviewer_skills.md"

def load_system_prompt() -> str:
    """起動時またはAPI呼び出し時に外部Markdownからプロンプトを読み込む"""
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        # 万が一ファイルが見つからない時のフェイルセーフ
        return (
            "You are an expert code reviewer. "
            "Output ONLY valid JSON matching the 5-axis schema (security, performance, maintainability, resilience, testability)."
        )

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

_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)

def _extract_json(raw: str) -> str:
    """Return the first top-level JSON object found in *raw*."""
    match = _JSON_OBJECT_RE.search(raw)
    if match is None:
        return raw  
    return match.group(0)

@router.post("/audit/ai", response_model=ReviewResponse)
async def run_ai_audit(request: ReviewRequest):
    """
    Runs an AI-powered code review using an LLM via litellm.
    Supports multi-file contextual review (Plan B).
    """
    if not request.target_paths:
        raise HTTPException(status_code=400, detail="No target paths provided.")

    combined_code_parts = []
    
    # 複数ファイルをループして読み込み、1つの巨大なテキストに合体させる
    for path_str in request.target_paths:
        target = Path(path_str)
        if not target.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Target path not found: {path_str}",
            )
        
        content = target.read_text(encoding="utf-8")
        # LLMがファイル境界を認識できるようにヘッダーをつける
        combined_code_parts.append(f"### File: {target.name}\n```python\n{content}\n```")

    code_content = "\n\n".join(combined_code_parts)

    user_message = (
        "Review the following code files together, checking for consistency, "
        "cross-file issues, and overall quality:\n\n"
        f"{code_content}"
    )
    
    if request.context:
        user_message = f"Context: {request.context}\n\n{user_message}"

    # 🌟 外部ファイルからプロンプトをロード
    system_prompt_text = load_system_prompt()

    try:
        llm_response = await litellm.acompletion(
            model=settings.REVIEW_MODEL,
            messages=[
                {"role": "system", "content": system_prompt_text},
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