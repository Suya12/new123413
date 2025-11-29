from pydantic import BaseModel


class Claim(BaseModel):
    id: int
    name: str                    # 피보험자 이름
    ssn: str                     # 주민번호
    phone: str                   # 연락처
    company: str                 # 보험사
    type: str                    # 청구유형
    status: str = "unchecked"    # unchecked | confirmed


class ClaimConfirmRequest(BaseModel):
    status: str
    key: str
    claim: Claim
