// Keep a trip list up to date from confirmation, change and cancellation emails.
// Usage: node parse-booking.js ../samples/flight-booking.eml ../samples/hotel-cancellation.eml

import { parseTravelEmail, readEml } from './focusllm.js';

const paths = process.argv.slice(2);
if (paths.length === 0) paths.push('../samples/flight-booking.eml', '../samples/hotel-cancellation.eml');

// Keyed by provider + booking_reference: a change email replaces the booking,
// a cancellation removes it.
const trips = new Map();

for (const path of paths) {
  const booking = await parseTravelEmail(await readEml(path));
  const key = `${booking.provider} / ${booking.booking_reference}`;
  console.log(`${path}: ${booking.booking_type} ${booking.status} — ${key}`);

  if (booking.status === 'cancelled') trips.delete(key);
  else trips.set(key, booking);
}

console.log('\nCurrent trips:');
for (const [key, booking] of trips) {
  const travellers = (booking.travellers ?? []).map((t) => t.name).join(', ');
  console.log(`\n${key} (${travellers}) — ${booking.total} ${booking.currency}`);
  // Times keep the local UTC offset ("+01:00"). Show the local part as-is,
  // and use Date only to sort or compare.
  const segments = [...booking.segments].sort((a, b) => new Date(a.start) - new Date(b.start));
  for (const s of segments) {
    console.log(`  ${s.number ?? ''} ${s.from} ${s.start} → ${s.to} ${s.end}`);
  }
}
