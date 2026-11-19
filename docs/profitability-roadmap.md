# EarnOrbit profitability roadmap

## Objective

Build a privacy-conscious, multi-source earning operations platform. The operator's aspirational benchmark is USD 1,000 net per month. This is a planning target, not a forecast or guarantee. The system must report verified results and must never label estimated or pending rewards as cash received.

## Current verified capabilities

- FastAPI service, SQLite persistence, bearer-token protected private endpoints.
- Opportunity registry and human-reviewed catalog.
- Conservative recommendation filter requiring active status, verified terms, official API, and explicit platform eligibility evidence.
- Revenue ledger with pending/confirmed/rejected states.
- Digital-product metadata workflow.
- Expense ledger with planned/paid/void states.
- Currency-separated gross revenue, paid expenses, and net totals.

## Privacy and identity handling

- Do not display the operator's legal name, residence, identity documents, KYC status, or personal eligibility profile in public pages, catalog entries, logs, analytics, or repository documentation.
- Collect the minimum personal information necessary. Keep any required eligibility profile private, access-controlled, and separate from public opportunity discovery.
- Do not publish identity documents or KYC artifacts to GitHub, application logs, analytics, or ordinary database exports.
- When a provider legally or contractually requires identity or residence verification, the user completes it directly with that provider using accurate information. The application must not falsify, conceal, or bypass required verification.
- Public opportunity records should describe provider requirements generically (for example, "identity verification may be required") and should not reveal the operator's personal profile.

## Next implementation phases

### Phase 1 — Profit truth and auditability
- Add expense ledger and currency-safe net profit summary (implemented in this branch).
- Keep pending earnings separate from confirmed earnings.
- Record platform terms evidence URL, review date, eligibility/KYC/payout requirement summary, and reviewer before activating any source.
- Add audit events for status changes and connector enable/disable operations.

### Phase 2 — Global opportunity intelligence
- Build source adapters only for documented public APIs, partner APIs, and explicitly permitted feeds.
- Normalize every candidate into a common record: platform, category, published eligibility requirements, identity/KYC requirements, payout rail, minimum payout, fees, API availability, terms URL, evidence date.
- Keep unknown or conflicting eligibility and payout evidence in pending review; never infer eligibility from IP, VPN, device location, or wallet location.
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

## Economics

A USD 1,000 monthly net target means approximately USD 33.33 net per calendar day. This arithmetic is only a target breakdown. Actual achievable income depends on accepted work volume, conversion/approval rates, time per task, fees, payout thresholds, provider reliability, and payout access. PTC-only activity is unlikely to be a dependable path to this target; the product should prioritize higher-value permitted work, microtasks, affiliate revenue, and original digital products when evidence supports them.

## Release gate

Do not call the system production-ready until CI passes, deployment secrets are configured outside Git, HTTPS is enabled, backups are tested, and at least one real provider integration has passed a terms and payout test without violating provider rules.


### Phase 2A — Monthly target optimizer (implemented in the active branch)
- Confidence-adjust opportunity economics using evidence completeness and evidence age.
- Label evidence as fresh (0–30 days), review due (31–90 days), or stale (over 90 days).
- Rank by confidence-adjusted net hourly estimate rather than raw reward rate alone.
- Add an authenticated monthly plan endpoint that calculates the remaining net target gap, daily pace, required net hourly pace, and source-level hours at each estimated rate.
- When no operator country is selected, only explicitly GLOBAL sources can enter the plan; never infer eligibility from network location.
- Keep estimates distinct from confirmed revenue and paid expenses. A mathematical fit is not a guarantee of task volume, acceptance, or payout.


### Phase 2B — Actual work-time feedback loop (implemented in the active branch)
- Record task duration and outcome independently from payout ledger entries.
- Calculate approved task value per tracked hour, task acceptance rate, pending value, rejected/abandoned time, and source-level productivity.
- Keep approved work value separate from confirmed cash revenue to avoid overstating income.
- Use measured performance to recalibrate estimated opportunity economics and stop spending time on low-yield sources.


### Phase 2C — Persistent source intake and activation gates (implemented in active branch)
- Persist candidate sources separately from approved opportunities.
- Record source category, discovery URL, official terms URL, evidence date, explicit eligibility scope, payout method/currency/minimum, fee, estimated task reward/time, and API availability.
- Promote a source only after a human review; promotion creates a pending opportunity and evidence history, never an active source.
- Require a separate explicit activation action with fresh evidence and known payout details.
- Keep manual-only opportunities visible as manual workflows while excluding them from automated API recommendations.
