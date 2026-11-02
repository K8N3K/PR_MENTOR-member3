"""Legacy review response used by the main branch frontend."""

from pydantic import BaseModel, Field


class ReviewAnalyzeRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2048)


class ReviewFindingResponse(BaseModel):
    severity: str
    title: str
    file: str
    line: int | str
    text: str
    proof: str | None = None
    status: str | None = None


class ReviewResponse(BaseModel):
    repository: str
    pull_request_title: str
    pull_request_number: int
    url: str | None = None
    review_id: str
    findings: list[ReviewFindingResponse]
    status: str = "completed"
