"""Turn an invoice or receipt email into a draft bill.

Usage: python parse_invoice.py ../samples/invoice.eml
"""

import json
import sys
from decimal import Decimal

from focusllm import parse_accounting_email, read_eml

path = sys.argv[1] if len(sys.argv) > 1 else "../samples/invoice.eml"
doc = parse_accounting_email(read_eml(path))

print(json.dumps(doc, indent=2, ensure_ascii=False))
print()

# Amounts come back as decimal strings ("64.90"): use Decimal, never float, for money.
amounts = doc.get("amounts") or {}
total = Decimal(amounts["total"]) if amounts.get("total") else None
supplier = (doc.get("supplier") or {}).get("name")

print(f"Type:      {doc['document_type']}")
print(f"Supplier:  {supplier}")
print(f"Number:    {doc.get('document_number')}")
print(f"Due:       {doc.get('due_date') or '—'}")  # null when the email doesn't say
print(f"Total:     {total} {doc.get('currency')}")
for line in doc.get("line_items") or []:
    print(f"  - {line['description']}: {line['quantity']} x {line['unit_price']} = {line['amount']}")
