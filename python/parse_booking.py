"""Keep a trip list up to date from confirmation, change and cancellation emails.

Usage: python parse_booking.py ../samples/flight-booking.eml ../samples/hotel-cancellation.eml
"""

import sys
from datetime import datetime

from focusllm import parse_travel_email, read_eml

paths = sys.argv[1:] or ["../samples/flight-booking.eml", "../samples/hotel-cancellation.eml"]

# Bookings keyed by (provider, booking_reference): a later change email replaces
# the segments, a cancellation removes the booking.
trips: dict[tuple[str, str], dict] = {}

for path in paths:
    booking = parse_travel_email(read_eml(path))
    key = (booking["provider"], booking["booking_reference"])
    print(f"{path}: {booking['booking_type']} {booking['status']} — {key[0]} / {key[1]}")

    if booking["status"] == "cancelled":
        trips.pop(key, None)
    else:
        trips[key] = booking

print("\nCurrent trips:")
for (provider, ref), booking in trips.items():
    travellers = ", ".join(t["name"] for t in booking.get("travellers") or [])
    print(f"\n{provider} — {ref} ({travellers}) — {booking.get('total')} {booking.get('currency')}")
    # Times keep the local UTC offset: show them as-is, convert to UTC only to sort.
    segments = sorted(booking["segments"], key=lambda s: datetime.fromisoformat(s["start"]))
    for s in segments:
        start = datetime.fromisoformat(s["start"])
        end = datetime.fromisoformat(s["end"])
        print(f"  {s.get('number') or ''} {s.get('from')} {start:%d %b %H:%M} → {s.get('to')} {end:%d %b %H:%M}")
