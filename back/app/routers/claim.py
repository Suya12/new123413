from fastapi import APIRouter, HTTPException

from app.models.claim import Claim
from app.services import claim as claim_service

router = APIRouter(prefix="/api/claims", tags=["Claims"])


@router.get("")
async def get_claims(status: str = "unchecked") -> list[Claim]:
    """청구 목록 조회 (status 필터링)"""
    return claim_service.get_claims_by_status(status)


@router.post("/{claim_id}/confirm")
async def confirm_claim(claim_id: int):
    """청구 확정 처리"""
    # 확정 전 청구 정보 조회해서 로그 출력
    claim = claim_service.get_claim_by_id(claim_id)
    if claim:
        print(f"✅ [확정 요청] id={claim.id}, 이름={claim.name}, 주민번호={claim.ssn}, 연락처={claim.phone}, 보험사={claim.company}, 유형={claim.type}")

    success = claim_service.confirm_claim(claim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Claim not found")

    print(f"✅ [확정 완료] claim_id={claim_id}")
    return {"ok": True}


@router.get("/{claim_id}")
async def get_claim(claim_id: int) -> Claim:
    """단일 청구 조회"""
    claim = claim_service.get_claim_by_id(claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
