import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from resume_review.documents import extract_resume_text
from resume_review.workflow import review_candidate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create evidence-based resume notes for a human reviewer."
    )
    parser.add_argument("--resume", required=True, type=Path, help="PDF or UTF-8 TXT resume")
    parser.add_argument(
        "--job-description", required=True, type=Path, help="UTF-8 text job-description file"
    )
    parser.add_argument(
        "--model",
        help="OpenAI chat model (defaults to OPENAI_MODEL or gpt-4o-mini)",
    )
    return parser


def main() -> int:
    load_dotenv()
    args = build_parser().parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY in the environment or .env file.", file=sys.stderr)
        return 2

    try:
        resume_text = extract_resume_text(args.resume.name, args.resume.read_bytes())
        job_description = args.job_description.read_text(encoding="utf-8").strip()
        if not job_description:
            raise ValueError("Job description cannot be empty.")
        model_name = args.model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        review = review_candidate(
            resume_text,
            job_description,
            model=ChatOpenAI(model=model_name, temperature=0),
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    except Exception as error:
        print(f"Review failed: {error}", file=sys.stderr)
        return 1

    print(review.model_dump_json(indent=2))
    return 0