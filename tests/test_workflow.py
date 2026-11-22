import pytest
from langchain_core.runnables import RunnableLambda

from resume_review.models import CandidateReview, RequirementEvidence
from resume_review.workflow import review_candidate


class FakeModel:
    def with_structured_output(self, schema):
        assert schema is CandidateReview
        return RunnableLambda(
            lambda _: CandidateReview(
                factual_summary="The resume states five years of Python experience.",
                requirement_evidence=[
                    RequirementEvidence(
                        requirement="Python experience",
                        status="evidence_found",
                        evidence="Five years building Python services.",
                    )
                ],
                review_notes=[],
            )
        )


def test_review_graph_returns_evidence_without_disposition():
    review = review_candidate(
        "Five years building Python services.",
        "Experience with Python.",
        model=FakeModel(),
    )

    assert review.requirement_evidence[0].status == "evidence_found"
    assert review.requirement_evidence[0].evidence == "Five years building Python services."
    assert not hasattr(review, "recommendation")


@pytest.mark.parametrize(
    ("resume_text", "job_description", "message"),
    [
        (" ", "Python role", "Resume text cannot be empty"),
        ("Python developer", " ", "Job description cannot be empty"),
    ],
)
def test_review_requires_both_documents(resume_text, job_description, message):
    with pytest.raises(ValueError, match=message):
        review_candidate(resume_text, job_description, model=FakeModel())