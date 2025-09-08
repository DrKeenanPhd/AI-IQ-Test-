from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets

router = APIRouter()

# In-memory store for expediency. Replace with Supabase table `tokens`.
_tokens_db: Dict[str, Dict[str, Any]] = {}

DEFAULT_TTL_HOURS = 16

class CreateTokenRequest(BaseModel):
    user_id: str
    ttl_hours: Optional[int] = DEFAULT_TTL_HOURS
    purpose: Optional[str] = "dashboard_access"  # e.g., dashboard_access, results_view

class CreateTokenResponse(BaseModel):
    token: str
    user_id: str
    created_at: str
    expires_at: str
    purpose: Optional[str] = None

class ValidateTokenRequest(BaseModel):
    token: str
    consume: Optional[bool] = False  # if true, mark as used upon successful validation

class ValidateTokenResponse(BaseModel):
    valid: bool
    reason: Optional[str] = None
    user_id: Optional[str] = None
    expires_at: Optional[str] = None
    used: Optional[bool] = None

class UseTokenRequest(BaseModel):
    token: str

class UseTokenResponse(BaseModel):
    success: bool
    reason: Optional[str] = None
    user_id: Optional[str] = None


def _now() -> datetime:
    return datetime.utcnow()


def _create_token_record(user_id: str, ttl_hours: int, purpose: Optional[str]) -> Dict[str, Any]:
    token = secrets.token_urlsafe(32)
    created_at = _now()
    expires_at = created_at + timedelta(hours=max(1, ttl_hours))
    record = {
        "token": token,
        "user_id": user_id,
        "created_at": created_at,
        "expires_at": expires_at,
        "used": False,
        "purpose": purpose,
    }
    _tokens_db[token] = record
    return record


def _validate_token(token: str) -> Dict[str, Any]:
    rec = _tokens_db.get(token)
    if not rec:
        return {"valid": False, "reason": "not_found"}
    if rec["used"]:
        return {"valid": False, "reason": "used", "user_id": rec["user_id"], "expires_at": rec["expires_at"].isoformat()}
    if _now() > rec["expires_at"]:
        return {"valid": False, "reason": "expired", "user_id": rec["user_id"], "expires_at": rec["expires_at"].isoformat()}
    return {"valid": True, "user_id": rec["user_id"], "expires_at": rec["expires_at"].isoformat(), "used": rec["used"]}


@router.post("/tokens", response_model=CreateTokenResponse)
def create_token(req: CreateTokenRequest):
    rec = _create_token_record(req.user_id, req.ttl_hours or DEFAULT_TTL_HOURS, req.purpose)
    return CreateTokenResponse(
        token=rec["token"],
        user_id=rec["user_id"],
        created_at=rec["created_at"].isoformat(),
        expires_at=rec["expires_at"].isoformat(),
        purpose=rec.get("purpose"),
    )


@router.post("/tokens/validate", response_model=ValidateTokenResponse)
def validate_token(req: ValidateTokenRequest):
    result = _validate_token(req.token)
    if not result.get("valid"):
        return ValidateTokenResponse(valid=False, reason=result.get("reason"))
    if req.consume:
        _tokens_db[req.token]["used"] = True
    return ValidateTokenResponse(
        valid=True,
        user_id=result.get("user_id"),
        expires_at=result.get("expires_at"),
        used=_tokens_db[req.token]["used"],
    )


@router.post("/tokens/use", response_model=UseTokenResponse)
def use_token(req: UseTokenRequest):
    result = _validate_token(req.token)
    if not result.get("valid"):
        return UseTokenResponse(success=False, reason=result.get("reason"))
    _tokens_db[req.token]["used"] = True
    return UseTokenResponse(success=True, user_id=result.get("user_id"))
