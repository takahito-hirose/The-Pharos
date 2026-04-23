# ARK_MEMORY_SYSTEM_ACTIVE
from fastapi import APIRouter
from models.schemas import StaticAuditRequest

router = APIRouter()

@router.post("/audit/static")
async def run_static_audit(request: StaticAuditRequest):
    """
    Runs a static analysis on the given target path.
    This is a mocked endpoint for now.
    """
    return {
        "status": "success",
        "score": 100,
        "message": f"Static analysis mocked for path: {request.target_path}"
    }