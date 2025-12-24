from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.trust_engine.orchestrator_async import AsyncAuditOrchestrator
from app.fastapi_app.dependencies import get_db, require_login, require_admin
from app.models_async.auth import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/v2/trust", tags=["Neuro-Verified Trust Engine"])

class AppealRequest(BaseModel):
    listing_id: str
    reason: str
    admin_override: bool = False

@router.post("/audit/{listing_id}")
async def trigger_manual_audit(
    listing_id: str, 
    strain_name: str, 
    listing_hash: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """
    Manually trigger the Neuro-Verified Audit for a listing.
    Requires login. Merchant ID is inferred from current user for manual triggers.
    """
    orchestrator = AsyncAuditOrchestrator(db)
    # Using current_user.username/id as merchant_addr proxy for manual triggers
    merchant_id = str(current_user.id) 
    
    result = await orchestrator.process_audit_request(
        trigger_type="MANUAL_TRIGGER", 
        listing_hash=listing_hash, 
        merchant_addr=merchant_id, 
        strain_name=strain_name
    )
    return result

@router.post("/appeal/{listing_id}")
async def submit_appeal(
    listing_id: str, 
    request: AppealRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Submit an appeal for a failed audit.
    Requires Admin privileges for the immediate override.
    """
    if request.admin_override:
        orchestrator = AsyncAuditOrchestrator(db)
        result = await orchestrator.process_appeal(listing_id, request.reason, current_user.username)
        return result
    
    return {"status": "APPEAL_SUBMITTED", "message": "Appeal under review by Trust Safety Team."}
