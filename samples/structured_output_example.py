"""Generic example: validate LLM output as structured JSON before using it.

`call_llm` is a stand-in for any LLM client function that takes a prompt
string and returns text. The prompt here is a placeholder, not a real one.
"""
import json
from dataclasses import dataclass

VALID_STATUS = {"out", "questionable", "probable"}


@dataclass
class InjuryReport:
    player: str
    status: str
    note: str


def parse_reports(raw: str) -> list[InjuryReport]:
    """Parse and validate the model's JSON. Raises on anything unexpected."""
    data = json.loads(raw)
    reports = []
    for item in data["reports"]:
        status = item["status"].lower()
        if status not in VALID_STATUS:
            raise ValueError(f"unexpected status: {status}")
        reports.append(InjuryReport(item["player"], status, item.get("note", "")))
    return reports


def extract_reports(text: str, call_llm, retries: int = 2) -> list[InjuryReport]:
    """Ask for JSON, validate it, and retry with the error if it is malformed."""
    prompt = (
        "Extract injury reports from the text below as JSON with a 'reports' "
        "list of objects with player, status, and note.\n\n" + text
    )
    last_error = None
    for _ in range(retries + 1):
        raw = call_llm(prompt)
        try:
            return parse_reports(raw)
        except (ValueError, KeyError, TypeError) as exc:
            last_error = exc
            prompt += f"\n\nThe previous output was invalid ({exc}). Return valid JSON only."
    raise RuntimeError(f"no valid output after {retries + 1} attempts") from last_error
