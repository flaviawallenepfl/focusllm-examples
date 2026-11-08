// Turn an invoice or receipt email into a draft bill.
// Usage: node parse-invoice.js ../samples/invoice.eml

import { parseAccountingEmail, readEml } from './focusllm.js';

const path = process.argv[2] ?? '../samples/invoice.eml';
const doc = await parseAccountingEmail(await readEml(path));

console.log(JSON.stringify(doc, null, 2), '\n');

// Amounts are decimal strings ("64.90"). Keep them as strings, or use a decimal
// library, rather than parseFloat, when you post them to a ledger.
console.log(`Type:      ${doc.document_type}`);
console.log(`Supplier:  ${doc.supplier?.name}`);
console.log(`Number:    ${doc.document_number}`);
console.log(`Due:       ${doc.due_date ?? '—'}`); // null when the email doesn't say
console.log(`Total:     ${doc.amounts?.total} ${doc.currency}`);
for (const line of doc.line_items ?? []) {
  console.log(`  - ${line.description}: ${line.quantity} x ${line.unit_price} = ${line.amount}`);
}
