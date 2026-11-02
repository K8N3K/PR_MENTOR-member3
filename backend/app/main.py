from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.review import router as review_router

app = FastAPI(title="PR Mentor API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(review_router)
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "pr-mentor"}
