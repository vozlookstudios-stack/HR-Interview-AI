from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.resume import router as resume_router


app = FastAPI(
    title="AI Interview Platform API",
    description="Backend for the AI Interview Avatar & Skill Assessment System",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Resume Intelligence API
app.include_router(resume_router)


@app.get("/")
async def root():
    return {
        "name": "AI Interview Platform",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Interview Backend",
    }