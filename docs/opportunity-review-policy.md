# Opportunity review and automation policy

EarnOrbit must not treat a website, social post, or marketing claim as proof that an earning opportunity is available or pays reliably.

## Approval gates
An opportunity can appear in the automated recommendation queue only when all are true:
- Status is `active` after a human review.
- Current terms and country eligibility have been checked and recorded.
- An official API or explicitly authorized integration exists.
- Payout method and minimum payout are known well enough to explain to the user.

## Country handling
- `GLOBAL` means the platform's current official terms explicitly allow the relevant country.
- A two-letter country code means the platform's current terms explicitly allow that country.
- `unknown` is not equivalent to global and must not pass a country-specific filter.
- Do not infer eligibility from IP address or approximate device location.
- Re-check identity verification, sanctions, tax, payout-provider and account-residency rules before activation.

## Automation boundaries
Allowed: official API calls, permitted affiliate links, user-authorized account connections, public documentation checks, ledger updates, and reminders.
Disallowed: fake clicks, artificial impressions, automated ad views, CAPTCHA bypass, account farming, traffic manipulation, or bypassing geographic restrictions.

## Scoring
The recommendation score is a transparent review-priority score based on verified terms, official API availability, crypto payout support, and explicitly global eligibility. It is not a prediction of income, reliability, or investment return.

## Re-verification
Store the source URL and date of each terms review in the opportunity notes. Re-verify before enabling a connector and periodically thereafter. If terms or eligibility cannot be confirmed, pause the opportunity.
