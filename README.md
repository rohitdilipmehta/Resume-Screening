# Resume Review Assistant

A command-line tool that helps a human reviewer summarize a resume and locate resume evidence related to requirements in a job description. It does not rank, recommend, shortlist, or reject candidates.

## Requirements

- Python 3.11 or newer
- An OpenAI API key

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

Add your key to `.env`. The default model is `gpt-4o-mini`; set `OPENAI_MODEL` there to use another supported OpenAI chat model.

## Use

```bash
resume-review --resume ./resume.pdf --job-description ./job-description.txt
```

The command prints a JSON summary and evidence table to stdout. Resume files may be PDF or UTF-8 TXT; job descriptions must be UTF-8 text. Documents are read locally and sent to OpenAI for analysis, but are not saved by this tool. Scanned PDFs require OCR before use.

The output reports evidence found in the resume, evidence not found, and unclear items. Missing evidence is not evidence that a person lacks a qualification. Verify every quotation against the source documents. The analysis can be incomplete or incorrect and must not be used as the basis for an employment decision; a qualified human reviewer must evaluate the original materials.

Review your organization's privacy, consent, retention, and security requirements before using real applicant data. Do not use this tool to infer protected or sensitive traits.

## Tests

```bash
python -m pip install -e ".[dev]"
pytest
```

## Project layout

```text
src/resume_review/
  cli.py
  documents.py
  models.py
  workflow.py
tests/
```

`LangGraph_candidate_screening.ipynb` is the original Colab prototype. The package here retains its LangGraph-based analysis, but replaces automatic interview/rejection routing with evidence-based notes for human review.
