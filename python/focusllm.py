"""Tiny FocusLLM client: one function per endpoint, nothing else.

FocusLLM endpoints all take the same input: a raw MIME email and an optional
list of extra fields. This module wraps that in a few lines with `requests`.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests

BASE_URL = os.environ.get("FOCUSLLM_BASE_URL", "https://api.focusllm.dev")


class FocusLLMError(RuntimeError):
    def __init__(self, status: int, body: str):
        super().__init__(f"FocusLLM returned HTTP {status}: {body[:500]}")
        self.status = status
        self.body = body


def read_eml(path: str | Path) -> str:
    """Read an .eml file as raw text, keeping its line endings untouched."""
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        return f.read()


def _post(endpoint: str, raw_email: str, fields: list[dict[str, str]] | None, timeout: float) -> dict[str, Any]:
    api_key = os.environ.get("FOCUSLLM_API_KEY")
    if not api_key:
        raise SystemExit("Set FOCUSLLM_API_KEY first (see .env.example).")

    payload: dict[str, Any] = {"raw_email": raw_email}
    if fields:
        payload["fields"] = fields

    response = requests.post(
        f"{BASE_URL}{endpoint}",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=timeout,
    )
    if not response.ok:
        raise FocusLLMError(response.status_code, response.text)
    return response.json()


def parse_accounting_email(raw_email: str, fields: list[dict[str, str]] | None = None, timeout: float = 60) -> dict[str, Any]:
    """POST /v1/email-parsing-accounting — invoices, receipts, credit notes..."""
    return _post("/v1/email-parsing-accounting", raw_email, fields, timeout)


def parse_travel_email(raw_email: str, fields: list[dict[str, str]] | None = None, timeout: float = 60) -> dict[str, Any]:
    """POST /v1/email-parsing-travel — flights, hotels, trains, car rentals..."""
    return _post("/v1/email-parsing-travel", raw_email, fields, timeout)
