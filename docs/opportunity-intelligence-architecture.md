# EarnOrbit opportunity intelligence architecture

## Data flow

1. **Intake** — an operator records a platform or task source. New sources remain pending by default.
2. **Evidence review** — the operator stores a first-party terms/evidence URL, review timestamp, explicit country scope, KYC summary, payout rail, minimum payout, fee, typical reward, task duration, and approval rate.
3. **Normalization** — evidence is stored as immutable review records, allowing later reviews to supersede earlier records without silently overwriting history.
4. **Economics** — estimated approved net hourly yield is calculated as:

   `average reward × (1 − payout fee %) × approval rate % × 60 ÷ task minutes`

   The result is denominated in the source payout currency. There is no implicit FX conversion.
5. **Ranking** — only opportunities with evidence are included. A country filter accepts an explicit matching country code or `GLOBAL`; unknown eligibility is excluded.
6. **Audit** — opportunity intake, evidence submission, revenue entries, and expense entries create append-only audit events.

## Interpretation rules

- Estimated net hourly yield is a planning estimate, not realized earnings, not a promise, and not a substitute for tracking actual time and cash-outs.
- The approval rate and average reward must be updated from the operator's own completed task history when possible.
- If the provider does not publish a fee, minimum payout, or country scope, record it as unknown instead of guessing.
- Do not compare hourly estimates across different currencies without a separately sourced FX rate and timestamp.
- Keep pending rewards separate from confirmed payouts. Confirmed means received and reconciled, not merely approved on a provider dashboard.

## Review freshness

A reviewer should re-check first-party terms before activating a source and whenever payout rules, eligibility, verification, or fees change. The review date and evidence URL are retained per record. A stale review should be treated as pending until refreshed.

## Current limitations

- The evidence record is manually entered; the repository does not yet run a global crawler or claim that the cited source has been independently fetched.
- The audit log records application events, but is not yet tamper-evident or externally backed up.
- There are no live provider API adapters or automatic payout reconciliations yet.
- Multi-user reviewer identity, role-based access, encrypted provider credentials, and production database migrations are future release gates.
