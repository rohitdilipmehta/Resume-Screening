import os

import streamlit as st
from dotenv import load_dotenv

from resume_review.documents import extract_resume_text
from resume_review.workflow import review_candidate


def load_streamlit_secrets() -> None:
    for name in ("OPENAI_API_KEY", "OPENAI_MODEL"):
        if os.getenv(name):
            continue
        try:
            value = st.secrets[name]
        except Exception:
            continue
        os.environ[name] = str(value)


load_dotenv()
st.set_page_config(page_title="Resume Review Assistant", page_icon="📄", layout="wide")
st.title("Resume Review Assistant")
st.caption(
    "Evidence-based notes for human review. This tool does not rank, recommend, "
    "shortlist, or reject candidates."
)
st.info(
    "The resume and job description are sent to OpenAI for analysis. Confirm your "
    "organization's privacy and applicant-data requirements before proceeding."
)

with st.form("review_form"):
    uploaded_resume = st.file_uploader("Resume (PDF or TXT)", type=["pdf", "txt"])
    job_description = st.text_area("Job description", height=240)
    submitted = st.form_submit_button("Create review summary", type="primary")

if submitted:
    load_streamlit_secrets()
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Set OPENAI_API_KEY in the app's Secrets settings or in your local .env file.")
    elif uploaded_resume is None:
        st.error("Upload a PDF or TXT resume.")
    elif uploaded_resume.size > 10 * 1024 * 1024:
        st.error("The resume must be smaller than 10 MB.")
    elif not job_description.strip():
        st.error("Paste a job description to compare against the resume evidence.")
    else:
        try:
            resume_text = extract_resume_text(uploaded_resume.name, uploaded_resume.getvalue())
            with st.spinner("Preparing evidence for human review..."):
                review = review_candidate(resume_text, job_description)

            st.subheader("Resume summary")
            st.write(review.factual_summary)

            st.subheader("Requirement evidence")
            if review.requirement_evidence:
                st.dataframe(
                    [
                        {
                            "Job requirement": item.requirement,
                            "Evidence status": item.status,
                            "Resume quotation": item.evidence,
                        }
                        for item in review.requirement_evidence
                    ],
                    hide_index=True,
                )
            else:
                st.write("No requirements were returned for review.")

            if review.review_notes:
                st.subheader("Items to verify")
                for note in review.review_notes:
                    st.write(f"- {note}")

            st.caption(
                "Verify quotations against the original resume. Missing evidence does not mean "
                "the candidate lacks a qualification. A human reviewer must make all employment "
                "decisions."
            )
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("Review failed. Check the API key and model settings, then try again.")