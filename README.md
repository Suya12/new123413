# 보험 청구 OCR 검증 시스템

보험금 청구 신청서를 OCR(광학 문자 인식)로 자동 추출한 후, 인식 결과를 검증하고 수정할 수 있는 웹 기반 관리 시스템입니다.

## 프로젝트 구조

```
캡스톤/
├── back/                          # 백엔드 (FastAPI)
│   ├── app/
│   │   ├── models/
│   │   │   └── claim.py          # Claim 데이터 모델
│   │   ├── routers/
│   │   │   └── claim.py          # API 라우터
│   │   └── services/
│   │       └── claim.py          # 비즈니스 로직
│   ├── main.py                    # FastAPI 진입점
│   └── requirements.txt           # Python 의존성
│
├── claim-app-frontend/            # 프론트엔드 (React + Vite)
│   ├── src/
│   │   ├── page/
│   │   │   ├── New_unchecked_claims.jsx   # 미확인 청구 목록
│   │   │   └── Ocr_compare.jsx            # OCR 비교/수정
│   │   ├── component/
│   │   │   └── FieldBlock.jsx    # 입력 필드 컴포넌트
│   │   ├── lib/
│   │   │   └── api.js            # Axios API 설정
│   │   └── App.jsx               # 라우팅 설정
│   └── package.json
│
└── README.md
```

## 기술 스택

### 프론트엔드
- **React** 19.1.1 - UI 라이브러리
- **React Router DOM** 7.9.5 - 클라이언트 라우팅
- **Axios** 1.13.2 - HTTP 클라이언트
- **Vite** 7.1.7 - 빌드 도구

### 백엔드
- **FastAPI** 0.122.0 - 웹 프레임워크
- **Uvicorn** 0.38.0 - ASGI 서버
- **Pydantic** 2.12.5 - 데이터 검증

## 설치 및 실행

### 백엔드 설정

```bash
cd back

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload --port 8000
```

### 프론트엔드 설정

```bash
cd claim-app-frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

개발 서버는 기본적으로 http://localhost:5173 에서 실행됩니다.

## 주요 기능

### 1. 미확인 청구 목록 페이지 (`/`)
- 상태가 "unchecked"인 청구건 목록 조회
- 2초 간격 폴링으로 실시간 목록 업데이트
- 테이블 형식으로 피보험자 정보 표시
- 셀 클릭 시 OCR 크롭 이미지 확인 가능
- [수정] 버튼: OCR 비교 페이지로 이동
- [확정] 버튼: 청구 확정 처리

### 2. OCR 비교/수정 페이지 (`/ocr_compare`)
- 왼쪽: 원본 이미지 (확대/축소/드래그 지원)
- 오른쪽: 추출된 데이터 수정 폼
  - **피보험자 정보**: 성명, 연락처, 주민등록번호, 통신사, 보험사
  - **수익자 정보**: 성명, 연락처, 주민등록번호, 통신사
  - **계좌 정보**: 은행명, 예금주, 계좌번호
- 각 필드별 OCR 크롭 이미지 확인
- 실시간 입력 검증 (연락처, 주민번호 형식)
- 되돌리기 기능

### 3. 외부 OCR 콜백 수신
- POST `/api/claims/callback` 엔드포인트로 외부 OCR 서버 응답 수신
- 한글 키를 영문 키로 자동 매핑

## API 엔드포인트

| 메소드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/claims?status=unchecked` | 상태별 청구 목록 조회 |
| GET | `/api/claims/{claim_id}` | 단일 청구 조회 |
| POST | `/api/claims/{claim_id}/confirm` | 청구 확정 처리 |
| POST | `/api/claims/callback` | 외부 OCR 콜백 수신 |

## 데이터 모델

### Claim
- **기본 정보**: id, client_request_id, status, request_image_base64
- **피보험자 정보**: 이름, 연락처, 주민번호, 통신사, 보험사 (+ 각 필드별 크롭 이미지)
- **수익자 정보**: 이름, 연락처, 주민번호, 통신사 (+ 각 필드별 크롭 이미지)
- **계좌 정보**: 은행명, 예금주, 계좌번호 (+ 각 필드별 크롭 이미지)

## 사용자 흐름

```
외부 OCR 서버 → POST /api/claims/callback → 백엔드 저장
                                              ↓
프론트엔드 ← GET /api/claims?status=unchecked ← 폴링(2초)
    ↓
미확인 청구 목록 표시
    ↓
[수정] → OCR 비교 페이지에서 데이터 검증/수정
    ↓
[확정] → POST /api/claims/{id}/confirm → 상태 변경 (confirmed)
```

## 개발 환경 설정

### CORS 설정
백엔드는 다음 오리진에서의 요청을 허용합니다:
- `http://localhost:5173`
- `http://localhost:5174`

### 환경 변수
현재는 별도의 환경 변수 설정 없이 기본값으로 동작합니다.

## 스크립트

### 프론트엔드
```bash
npm run dev      # 개발 서버 실행
npm run build    # 프로덕션 빌드
npm run preview  # 빌드 미리보기
npm run lint     # ESLint 실행
```

### 백엔드
```bash
uvicorn main:app --reload           # 개발 모드
uvicorn main:app --host 0.0.0.0     # 외부 접근 허용
```
