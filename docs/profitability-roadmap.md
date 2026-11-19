# EarnOrbit profitability roadmap

## Objective

Build a trustworthy multi-source earning operations platform. The operator's aspirational benchmark is USD 1,000 net per month. This is a planning target, not a forecast or guarantee. The system must report verified results and must never label estimated or pending rewards as cash received.

## Current verified capabilities

- FastAPI service, SQLite persistence, bearer-token protected private endpoints.
- Opportunity registry and human-reviewed catalog.
- Conservative recommendation filter requiring active status, verified terms, official API, and explicit country eligibility.
- Revenue ledger with pending/confirmed/rejected states.
- Digital-product metadata workflow.
- Expense ledger with planned/paid/void states.
- Currency-separated gross revenue, paid expenses, and net totals.

## Next implementation phases

### Phase 1 — Profit truth and auditability
- Add expense ledger and currency-safe net profit summary (implemented in this branch).
- Keep pending earnings separate from confirmed earnings.
- Record platform terms evidence URL, review date, country/KYC/payout checks, and reviewer before activating any source.
- Add audit events for status changes and connector enable/disable operations.

### Phase 2 — Global opportunity intelligence
- Build source adapters only for documented public APIs, partner APIs, and explicitly permitted feeds.
- Normalize every candidate into a common record: platform, category, countries, identity/KYC rules, payout rail, minimum payout, fees, API availability, terms URL, evidence date.
- Keep unknown or conflicting country/payout evidence in pending review; never infer eligibility from IP or VPN.
- Rank by verified net yield, minimum payout, time burden, reliability evidence, and withdrawal friction. A ranking score is not a promise of income.

### Phase 3 — Permitted task operations
- Support user-authorized official API tasks, affiliate reporting, survey/task status sync where the provider explicitly permits it, and reminder queues.
- Use human confirmation for account login, identity checks, sensitive actions, and irreversible withdrawals.
- Do not automate ad clicks, impressions, CAPTCHA, account creation/farming, or geographic restriction bypass.

### Phase 4 — Payout reconciliation
- Import payout confirmations using official provider APIs or user-supplied transaction references.
- Reconcile platform balances against wallet/exchange deposits; never request or store seed phrases/private keys.
- Report gross, fees, net received, pending, rejected, and cash-out status separately.

### Phase 5 — Operations and scale
- Multi-user roles, encrypted secret management, HTTPS deployment, backups, monitoring, rate limits, and retention controls.
- Add an operator-configured monthly target and weekly performance review based on actual verified data.

## Country and legal safeguards

The current project policy uses the operator-provided Iran residence/identity profile (IR). Do not silently change this based on IP, VPN, device location, or wallet location. A platform must be checked against current first-party terms for residence, KYC documents, ongoing use, payout eligibility, and payout provider. If terms are silent, stale, or ambiguous, keep it pending. No false address, borrowed identity, VPN evasion, or nominee account.

## Economics

A USD 1,000 monthly net target means approximately USD 33.33 net per calendar day. This arithmetic is only a target breakdown. Actual achievable income depends on country eligibility, accepted work volume, conversion/approval rates, time per task, fees, payout thresholds, and platform demand. PTC-only activity is unlikely to be a dependable path to this target; the product should prioritize higher-value permitted work, affiliate revenue, and original digital products when evidence supports them.

## Release gate

Do not call the system production-ready until CI passes, deployment secrets are configured outside Git, HTTPS is enabled, backups are tested, and at least one real provider integration has passed a terms and payout test without violating provider rules.
