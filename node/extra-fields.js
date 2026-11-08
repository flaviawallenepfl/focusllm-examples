// Ask for values outside the fixed schema with the optional `fields` input.
// Usage: node extra-fields.js

import { parseAccountingEmail, parseTravelEmail, readEml } from './focusllm.js';

const invoice = await parseAccountingEmail(await readEml('../samples/invoice.eml'), {
  fields: [
    { name: 'po_number', description: 'The purchase order number quoted on the invoice, such as PO-1234.' },
    { name: 'cost_centre', description: 'The internal cost centre, if the email mentions one.' },
  ],
});
console.log('Invoice extra fields:', invoice.fields);

const booking = await parseTravelEmail(await readEml('../samples/flight-booking.eml'), {
  fields: [{ name: 'seat', description: 'The seat number for each flight, such as 14C, if the email gives one.' }],
});
console.log('Booking extra fields:', booking.fields);
