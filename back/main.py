from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import claim

app = FastAPI()

# CORS (리액트에서 호출하려면 거의 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 리액트 개발 주소 (Vite 기본)
        "http://localhost:5173",  # Vite 기본 포트
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(claim.router)
