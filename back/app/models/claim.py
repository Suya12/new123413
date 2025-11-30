from pydantic import BaseModel, Field
from typing import Optional


class Claim(BaseModel):
    id: int
    client_request_id: str
    status: str = "unchecked"    # unchecked | confirmed
    request_image_base64: Optional[str] = None

    # 피보험자 정보
    insured_name: str                          # 피보험자 성명
    insured_name_crop: Optional[str] = None
    insured_contact: str                       # 피보험자 연락처
    insured_contact_crop: Optional[str] = None
    insured_carrier: str                       # 피보험자 통신사
    insured_carrier_crop: Optional[str] = None
    insured_ssn: str                          # 피보험자 주민등록번호
    insured_ssn_crop: Optional[str] = None
    insured_insurance_company: str             # 피보험자 수익자청구 요청 보험사
    insured_insurance_company_crop: Optional[str] = None

    # 수익자 정보
    beneficiary_name: str                      # 수익자 성명
    beneficiary_name_crop: Optional[str] = None
    beneficiary_ssn: str                      # 수익자 주민등록번호
    beneficiary_ssn_crop: Optional[str] = None
    beneficiary_contact: str                   # 수익자 연락처
    beneficiary_contact_crop: Optional[str] = None
    beneficiary_carrier: str                   # 수익자 통신사
    beneficiary_carrier_crop: Optional[str] = None

    # 보험금 지급 정보
    payment_bank: str                          # 보험금 지급 은행명
    payment_bank_crop: Optional[str] = None
    payment_account_holder: str                # 보험금 지급 예금주 성함
    payment_account_holder_crop: Optional[str] = None
    payment_account_number: str                # 보험금 지급 계좌번호
    payment_account_number_crop: Optional[str] = None


class ClaimConfirmRequest(BaseModel):
    status: str
    key: str
    claim: Claim


class ExtractedField(BaseModel):
    """OCR 추출 필드 (text, cropped_bytes, confidence)"""
    text: str
    cropped_bytes: Optional[str] = None
    confidence: Optional[float] = None


class ExternalCallbackResponse(BaseModel):
    """외부 서버로부터 받는 콜백 응답"""
    client_request_id: str
    status: str
    request_image_base64: str
    cropped_bytes: Optional[str] = None

    # 띄어쓰기가 있는 키 이름 (도커에서 보내는 형식)
    피보험자_성명: ExtractedField = Field(alias="피보험자 성명")
    피보험자_연락처: ExtractedField = Field(alias="피보험자 연락처")
    피보험자_통신사: ExtractedField = Field(alias="피보험자 통신사")
    피보험자_주민등록번호: ExtractedField = Field(alias="피보험자 주민등록번호")
    피보험자_수익자청구_요청_보험사: ExtractedField = Field(alias="피보험자 수익자청구 요청 보험사")
    수익자_성명: ExtractedField = Field(alias="수익자 성명")
    수익자_주민등록번호: ExtractedField = Field(alias="수익자 주민등록번호")
    수익자_연락처: ExtractedField = Field(alias="수익자 연락처")
    수익자_통신사: ExtractedField = Field(alias="수익자 통신사")
    보험금_지급_은행명: ExtractedField = Field(alias="보험금 지급 은행명")
    보험금_지급_예금주_성함: ExtractedField = Field(alias="보험금 지급 예금주 성함")
    보험금_지급_계좌번호: ExtractedField = Field(alias="보험금 지급 계좌번호")
