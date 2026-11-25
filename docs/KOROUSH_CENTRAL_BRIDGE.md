# KOROUSH CENTRAL AI bridge

This repository contains a dependency-free, manually triggered bridge to the shared KOROUSH CENTRAL AI service.

## Configure once

Add these repository Actions secrets (never commit their values):

- `KOROUSH_CENTRAL_BASE_URL`: HTTPS base URL of the central service.
- `KOROUSH_CENTRAL_TENANT_KEY`: tenant key restricted to this exact GitHub repository, with `jobs:enqueue`, `jobs:read`, and `inference:chat`.

The central administrator must approve this exact `owner/repository` identity and issue its tenant key. The bridge does not need the central admin key.

## Run

Open Actions → KOROUSH Central AI Bridge → Run workflow. Supply a stable idempotency key, optional target language, and a JSON array containing 1–8 evidence objects. Each item must include `source_id` and `text`; include `publisher`, `source_url`, and ISO-8601 `observed_at` for provenance.

Example shape (replace with real evidence; this is not a market claim):

```json
[
  {
    "source_id": "report-001",
    "publisher": "Publisher name",
    "source_url": "https://example.org/report",
    "observed_at": "2026-11-25T00:00:00Z",
    "text": "A short excerpt from the actual source."
  }
]
```

The bridge submits to the fixed `INTEGRATION_ID` research workflow, polls the tenant-scoped job status, and fails if the job fails or times out. It never logs the tenant key, fetches arbitrary source URLs, or performs account actions.

## Current limits

- Trigger is manual until the evidence-generation step is reviewed and wired to this repository's actual outputs.
- The central service must have its durable worker enabled and encrypted payload storage configured.
- No live trading, public video publishing, automated clicking, wallet signing, or payout action is enabled.
- A queued request is not proof that the model workflow completed; inspect the terminal job status.
