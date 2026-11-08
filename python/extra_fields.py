"""Ask for values outside the fixed schema with the optional `fields` input.

Usage: python extra_fields.py
"""

import json

from focusllm import parse_accounting_email, parse_travel_email, read_eml

invoice = parse_accounting_email(
    read_eml("../samples/invoice.eml"),
    fields=[
        {"name": "po_number", "description": "The purchase order number quoted on the invoice, such as PO-1234."},
        {"name": "cost_centre", "description": "The internal cost centre, if the email mentions one."},
    ],
)
print("Invoice extra fields:", json.dumps(invoice["fields"], indent=2))

booking = parse_travel_email(
    read_eml("../samples/flight-booking.eml"),
    fields=[{"name": "seat", "description": "The seat number for each flight, such as 14C, if the email gives one."}],
)
print("Booking extra fields:", json.dumps(booking["fields"], indent=2))
