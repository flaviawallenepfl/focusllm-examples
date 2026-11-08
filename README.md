# FocusLLM API examples

Runnable examples for the [FocusLLM](https://www.focusllm.dev/) email parsing APIs, in **curl**, **Python** and **Node.js**.

FocusLLM turns raw emails into structured JSON. Each use case is one endpoint at one price per call:

| Endpoint | What it returns | Price |
|---|---|---|
| [`POST /v1/email-parsing-accounting`](https://www.focusllm.dev/use-cases/email-parsing-accounting/) | Document type, supplier, number, dates, net/tax/total, line items, payment reference | $0.01 per successful call |
| [`POST /v1/email-parsing-travel`](https://www.focusllm.dev/use-cases/email-parsing-travel/) | Booking type, status, provider, reference, travellers, segments with ISO 8601 times, total | $0.01 per successful call |

> FocusLLM is in private alpha. Request an API key at [hello@focusllm.dev](mailto:hello@focusllm.dev?subject=API%20key%20request).

## How the API works

Every endpoint takes the same request:

```json
{
  "raw_email": "From: ...\r\nSubject: ...\r\n\r\n...",
  "fields": [
    { "name": "po_number", "description": "The purchase order number, such as PO-1234." }
  ]
}
```

- **`raw_email`** (string) — the full message as raw MIME text, attachments included. Send the `.eml` file as-is.
- **`fields`** (optional) — extra values to extract beyond the fixed schema. They come back under `fields` in the response.
- **Auth** — `Authorization: Bearer $FOCUSLLM_API_KEY`.
- A value that is not in the email comes back as **`null`** — never a guess.
- Amounts are **decimal strings** (`"64.90"`); handle them with a decimal type, not floats.

## Repository layout

```
samples/   Example emails (.eml) — invoice, HTML receipt, flight booking, hotel cancellation
curl/      Shell scripts (curl + jq)
python/    Small client + scripts (requests)
node/      Small client + scripts (built-in fetch, no dependencies)
```

## Setup

```bash
git clone https://github.com/<you>/focusllm-examples.git
cd focusllm-examples
cp .env.example .env        # then put your key in .env
export $(grep -v '^#' .env | xargs)
```

## curl

Requires `curl` and `jq`.

```bash
./curl/parse.sh accounting samples/invoice.eml
./curl/parse.sh travel     samples/flight-booking.eml
./curl/extra-fields.sh     # adds po_number and cost_centre
```

`jq -Rs '{raw_email: .}'` reads the whole `.eml` and escapes it into JSON, so the email is sent byte-for-byte.

## Python

Requires Python 3.9+.

```bash
cd python
pip install -r requirements.txt

python parse_invoice.py ../samples/invoice.eml           # draft bill from an invoice
python parse_booking.py                                  # trip list from booking + cancellation emails
python extra_fields.py                                   # custom fields
python batch_to_csv.py ../samples bills.csv              # a folder of emails → CSV
```

The client is [`python/focusllm.py`](python/focusllm.py):

```python
from focusllm import parse_accounting_email, read_eml

doc = parse_accounting_email(read_eml("invoice.eml"))
print(doc["supplier"]["name"], doc["amounts"]["total"], doc["currency"])
```

## Node.js

Requires Node 18+ (uses the built-in `fetch`).

```bash
cd node
node parse-invoice.js ../samples/invoice.eml
node parse-booking.js
node extra-fields.js
```

The client is [`node/focusllm.js`](node/focusllm.js):

```js
import { parseTravelEmail, readEml } from './focusllm.js';

const booking = await parseTravelEmail(await readEml('booking.eml'));
console.log(booking.booking_reference, booking.status, booking.segments);
```

## Tips

- **Keep line endings.** Read `.eml` files without newline conversion (`newline=""` in Python) so the MIME structure stays intact.
- **Travel times keep their local offset** (`2026-12-14T07:35:00+01:00` for a departure from Paris). Display them as-is; convert to UTC only to sort or compare.
- **Changes and cancellations.** Match on `provider` + `booking_reference`: replace the segments on `changed`, remove the booking on `cancelled` (see `parse_booking.py`).
- **Filter out noise.** The accounting endpoint returns `document_type: "other"` for emails that aren't bills, receipts, credit notes, statements or reminders (see `batch_to_csv.py`).
- **Never commit your key.** `.env` is in `.gitignore`.

## Links

- [FocusLLM website](https://www.focusllm.dev/)
- [Accounting API reference](https://www.focusllm.dev/use-cases/email-parsing-accounting/)
- [Travel API reference](https://www.focusllm.dev/use-cases/email-parsing-travel/)
- [Travel developer guide](https://www.focusllm.dev/use-cases/email-parsing-travel/developer-guide/)

## License

MIT — see [LICENSE](LICENSE).
