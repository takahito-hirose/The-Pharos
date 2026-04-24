# ARK_MEMORY_SYSTEM_ACTIVE
import subprocess
from pathlib import Path

from fastapi import APIRouter, HTTPException
from models.schemas import StaticAuditRequest, StaticAuditResponse

router = APIRouter()


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