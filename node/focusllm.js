// Tiny FocusLLM client for Node 18+ (uses the built-in fetch, no dependencies).

import { readFile } from 'node:fs/promises';

const BASE_URL = process.env.FOCUSLLM_BASE_URL ?? 'https://api.focusllm.dev';

export class FocusLLMError extends Error {
  constructor(status, body) {
    super(`FocusLLM returned HTTP ${status}: ${body.slice(0, 500)}`);
    this.status = status;
    this.body = body;
  }
}

/** Read an .eml file as raw text, line endings untouched. */
export const readEml = (path) => readFile(path, 'utf8');

async function post(endpoint, rawEmail, { fields, timeoutMs = 60_000 } = {}) {
  const apiKey = process.env.FOCUSLLM_API_KEY;
  if (!apiKey) throw new Error('Set FOCUSLLM_API_KEY first (see .env.example).');

  const body = { raw_email: rawEmail };
  if (fields?.length) body.fields = fields;

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(timeoutMs),
  });

  if (!response.ok) throw new FocusLLMError(response.status, await response.text());
  return response.json();
}

/** POST /v1/email-parsing-accounting — invoices, receipts, credit notes... */
export const parseAccountingEmail = (rawEmail, options) =>
  post('/v1/email-parsing-accounting', rawEmail, options);

/** POST /v1/email-parsing-travel — flights, hotels, trains, car rentals... */
export const parseTravelEmail = (rawEmail, options) =>
  post('/v1/email-parsing-travel', rawEmail, options);
