from app.models.claim import Claim

# 임시 저장소 (프로덕션에선 DB 사용)
claims_db: dict[int, Claim] = {}

# 초기 테스트 데이터
_initial_data = [
    Claim(id=1, name="배철수", ssn="123456-7890123", phone="010-5787-2222", company="라이나 생명", type="치아보험"),
    Claim(id=2, name="김철수", ssn="981010-1234567", phone="010-3333-4444", company="삼성화재", type="실손보험"),
    Claim(id=3, name="이영희", ssn="010101-3456789", phone="010-1111-2222", company="DB손해보험", type="암보험"),
    Claim(id=4, name="박민수", ssn="900101-1234567", phone="010-9999-8888", company="현대해상", type="실손보험"),
]

for c in _initial_data:
    claims_db[c.id] = c


def get_claims_by_status(status: str) -> list[Claim]:
    """상태별 청구 목록 조회"""
    return [c for c in claims_db.values() if c.status == status]


def get_claim_by_id(claim_id: int) -> Claim | None:
    """ID로 청구 조회"""
    return claims_db.get(claim_id)


def confirm_claim(claim_id: int) -> bool:
    """청구 확정 처리"""
    claim = claims_db.get(claim_id)
    if claim is None:
        return False
    claim.status = "confirmed"
    return True


def add_claim(claim: Claim) -> Claim:
    """새 청구 추가"""
    claims_db[claim.id] = claim
    return claim
