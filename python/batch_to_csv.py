"""Parse every .eml in a folder with the accounting endpoint and write a CSV.

Usage: python batch_to_csv.py ../samples bills.csv
"""

import csv
import sys
from pathlib import Path

from focusllm import FocusLLMError, parse_accounting_email, read_eml

folder = Path(sys.argv[1] if len(sys.argv) > 1 else "../samples")
out = Path(sys.argv[2] if len(sys.argv) > 2 else "bills.csv")

columns = ["file", "document_type", "supplier", "tax_id", "document_number",
           "issue_date", "due_date", "currency", "net", "tax", "total", "payment_reference"]

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for eml in sorted(folder.glob("*.eml")):
        try:
            doc = parse_accounting_email(read_eml(eml))
        except FocusLLMError as e:
            print(f"skip {eml.name}: {e}", file=sys.stderr)
            continue
        if doc["document_type"] == "other":
            print(f"skip {eml.name}: not an accounting document")
            continue
        supplier = doc.get("supplier") or {}
        amounts = doc.get("amounts") or {}
        writer.writerow({
            "file": eml.name,
            "document_type": doc["document_type"],
            "supplier": supplier.get("name"),
            "tax_id": supplier.get("tax_id"),
            "document_number": doc.get("document_number"),
            "issue_date": doc.get("issue_date"),
            "due_date": doc.get("due_date"),
            "currency": doc.get("currency"),
            "net": amounts.get("net"),
            "tax": amounts.get("tax"),
            "total": amounts.get("total"),
            "payment_reference": doc.get("payment_reference"),
        })
        print(f"ok   {eml.name}")

print(f"\nWrote {out}")
