from typing import Literal

from pydantic import BaseModel, Field


class RequirementEvidence(BaseModel):
    requirement: str = Field(description="A requirement stated in the supplied job description")
    status: Literal["evidence_found", "not_found_in_resume", "unclear"]
    evidence: str = Field(description="An exact resume quotation, or an empty string")


class CandidateReview(BaseModel):
    factual_summary: str = Field(
        description="A concise summary of facts explicitly stated in the resume"
    )
    requirement_evidence: list[RequirementEvidence] = Field(
        description="Evidence for job requirements, without ratings or recommendations"
    )
    review_notes: list[str] = Field(
        description="Ambiguities or items a human reviewer may want to verify"
    )