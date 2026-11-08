#!/usr/bin/env bash
# Send a raw .eml file to a FocusLLM endpoint and pretty-print the JSON.
#
# Usage:
#   ./curl/parse.sh accounting samples/invoice.eml
#   ./curl/parse.sh travel     samples/flight-booking.eml
#
# Requires: curl, jq, and FOCUSLLM_API_KEY in the environment.
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <accounting|travel> <file.eml>" >&2
  exit 1
fi

use_case="$1"
eml="$2"
base_url="${FOCUSLLM_BASE_URL:-https://api.focusllm.dev}"

case "$use_case" in
  accounting) endpoint="/v1/email-parsing-accounting" ;;
  travel)     endpoint="/v1/email-parsing-travel" ;;
  *) echo "Unknown use case: $use_case (expected accounting or travel)" >&2; exit 1 ;;
esac

: "${FOCUSLLM_API_KEY:?Set FOCUSLLM_API_KEY first (see .env.example)}"

# jq -Rs reads the whole file as one string and JSON-escapes it safely,
# so the email is sent byte-for-byte (line endings, quotes, accents included).
jq -Rs '{raw_email: .}' "$eml" \
  | curl --fail-with-body -sS "${base_url}${endpoint}" \
      -H "Authorization: Bearer ${FOCUSLLM_API_KEY}" \
      -H "Content-Type: application/json" \
      --data-binary @- \
  | jq .
