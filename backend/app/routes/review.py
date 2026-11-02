"""Review endpoints consumed by the default frontend."""

from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.github_service.client import GitHubServiceError
from app.github_service.parser import parse_pull_request_url
from app.github_service.pull_requests import ingest_pull_request
from app.database.reviews import get_review as load_review, list_reviews, save_review
from app.schemas.review import ReviewAnalyzeRequest
from app.services.review_orchestrator import run_review

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/analyze")
def analyze_pull_request(request: ReviewAnalyzeRequest):
    try:
        # Validate the URL before making any outbound request.
        parse_pull_request_url(request.url)
        result = run_review(ingest_pull_request(request.url))
        result["review_id"] = uuid4().hex
        save_review(result)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Review could not be completed. Configure the AI provider and try again.") from exc


@router.get("/history")
def history():
    return list_reviews()


@router.get("/{review_id}")
def get_review(review_id: str):
    review = load_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found.")
    return review
