from fastapi import APIRouter, HTTPException

from app.models.claim import Claim, ExternalCallbackResponse
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
        print(f"✅ [확정 요청] id={claim.id}, client_request_id={claim.client_request_id}")
        print(f"   피보험자: {claim.insured_name}, 주민번호={claim.insured_ssn}, 연락처={claim.insured_contact}")
        print(f"   보험사: {claim.insured_insurance_company}")

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


@router.post("/callback")
async def receive_external_callback(callback_data: ExternalCallbackResponse):
    """외부 서버로부터 콜백 응답 수신"""
    print(f"📩 [콜백 수신] client_request_id={callback_data.client_request_id}, status={callback_data.status}")

    # 외부 응답을 내부 Claim 모델로 변환
    claim = claim_service.process_external_callback(callback_data)

    print(f"✅ [청구 저장 완료] id={claim.id}, 피보험자={claim.insured_name}")

    return {"ok": True, "claim_id": claim.id}
