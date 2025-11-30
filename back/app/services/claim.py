from app.models.claim import Claim, ExternalCallbackResponse

# 임시 저장소 (프로덕션에선 DB 사용)
claims_db: dict[int, Claim] = {}

# ID 자동 증가를 위한 카운터
_next_id = 1

# 초기 테스트 데이터
_initial_data = [
    Claim(
        id=1,
        client_request_id="test_req_001",
        status="unchecked",
        insured_name="배철수",
        insured_contact="010-5787-2222",
        insured_carrier="SKT",
        insured_ssn="123456-7890123",
        insured_insurance_company="라이나 생명",
        beneficiary_name="배철수",
        beneficiary_ssn="123456-7890123",
        beneficiary_contact="010-5787-2222",
        beneficiary_carrier="SKT",
        payment_bank="신한은행",
        payment_account_holder="배철수",
        payment_account_number="110-123-456789"
    ),
    Claim(
        id=2,
        client_request_id="test_req_002",
        status="unchecked",
        insured_name="김철수",
        insured_contact="010-3333-4444",
        insured_carrier="KT",
        insured_ssn="981010-1234567",
        insured_insurance_company="삼성화재",
        beneficiary_name="김철수",
        beneficiary_ssn="981010-1234567",
        beneficiary_contact="010-3333-4444",
        beneficiary_carrier="KT",
        payment_bank="국민은행",
        payment_account_holder="김철수",
        payment_account_number="123-45-678901"
    ),
    Claim(
        id=3,
        client_request_id="test_req_003",
        status="unchecked",
        insured_name="이영희",
        insured_contact="010-1111-2222",
        insured_carrier="LG U+",
        insured_ssn="010101-3456789",
        insured_insurance_company="DB손해보험",
        beneficiary_name="이영희",
        beneficiary_ssn="010101-3456789",
        beneficiary_contact="010-1111-2222",
        beneficiary_carrier="LG U+",
        payment_bank="우리은행",
        payment_account_holder="이영희",
        payment_account_number="1002-123-456789"
    ),
]

for c in _initial_data:
    claims_db[c.id] = c
    if c.id >= _next_id:
        _next_id = c.id + 1


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


def process_external_callback(callback_data: ExternalCallbackResponse) -> Claim:
    """외부 서버 콜백 응답을 처리하여 Claim 객체로 변환 후 저장"""
    global _next_id

    # 한글 키를 영문 키로 매핑하여 Claim 객체 생성 (.text로 값, .cropped_bytes로 크롭 이미지 추출)
    claim = Claim(
        id=_next_id,
        client_request_id=callback_data.client_request_id,
        status="unchecked",
        request_image_base64=callback_data.request_image_base64,
        # 피보험자 정보
        insured_name=callback_data.피보험자_성명.text,
        insured_name_crop=callback_data.피보험자_성명.cropped_bytes,
        insured_contact=callback_data.피보험자_연락처.text,
        insured_contact_crop=callback_data.피보험자_연락처.cropped_bytes,
        insured_carrier=callback_data.피보험자_통신사.text,
        insured_carrier_crop=callback_data.피보험자_통신사.cropped_bytes,
        insured_ssn=callback_data.피보험자_주민등록번호.text,
        insured_ssn_crop=callback_data.피보험자_주민등록번호.cropped_bytes,
        insured_insurance_company=callback_data.피보험자_수익자청구_요청_보험사.text,
        insured_insurance_company_crop=callback_data.피보험자_수익자청구_요청_보험사.cropped_bytes,
        # 수익자 정보
        beneficiary_name=callback_data.수익자_성명.text,
        beneficiary_name_crop=callback_data.수익자_성명.cropped_bytes,
        beneficiary_ssn=callback_data.수익자_주민등록번호.text,
        beneficiary_ssn_crop=callback_data.수익자_주민등록번호.cropped_bytes,
        beneficiary_contact=callback_data.수익자_연락처.text,
        beneficiary_contact_crop=callback_data.수익자_연락처.cropped_bytes,
        beneficiary_carrier=callback_data.수익자_통신사.text,
        beneficiary_carrier_crop=callback_data.수익자_통신사.cropped_bytes,
        # 보험금 지급 정보
        payment_bank=callback_data.보험금_지급_은행명.text,
        payment_bank_crop=callback_data.보험금_지급_은행명.cropped_bytes,
        payment_account_holder=callback_data.보험금_지급_예금주_성함.text,
        payment_account_holder_crop=callback_data.보험금_지급_예금주_성함.cropped_bytes,
        payment_account_number=callback_data.보험금_지급_계좌번호.text,
        payment_account_number_crop=callback_data.보험금_지급_계좌번호.cropped_bytes,
    )

    _next_id += 1
    claims_db[claim.id] = claim

    return claim
