#!/usr/bin/env bash
# Ask for extra fields on top of the fixed schema, using the optional `fields` input.
#
# Usage: ./curl/extra-fields.sh
set -euo pipefail
cd "$(dirname "$0")/.."

base_url="${FOCUSLLM_BASE_URL:-https://api.focusllm.dev}"
: "${FOCUSLLM_API_KEY:?Set FOCUSLLM_API_KEY first (see .env.example)}"

jq -Rs '{
  raw_email: .,
  fields: [
    { name: "po_number",   description: "The purchase order number quoted on the invoice, such as PO-1234." },
    { name: "cost_centre", description: "The internal cost centre, if the email mentions one." }
  ]
}' samples/invoice.eml \
  | curl --fail-with-body -sS "${base_url}/v1/email-parsing-accounting" \
      -H "Authorization: Bearer ${FOCUSLLM_API_KEY}" \
      -H "Content-Type: application/json" \
      --data-binary @- \
  | jq '{document_number, amounts, fields}'
