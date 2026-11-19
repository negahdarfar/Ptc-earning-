# Initial source intake catalogue

This catalogue is a research shortlist, not an eligibility decision or endorsement. It does not imply that the operator can register or receive payouts. Verify current residence, identity, tax, payout and minimum thresholds directly before approval.

| Source | Category | Initial intake | Official starting point |
|---|---|---|---|
| Upwork | Client services | Manual workflow first; API access is gated and must not be assumed. | https://www.upwork.com/legal ; https://www.upwork.com/developer/documentation/graphql/api/docs/index.html |
| Fiverr | Productized services | Manual seller workflow; verify current terms and payment rules. | https://www.fiverr.com/legal-portal/legal-terms/terms-of-service |
| Gumroad | Original digital products | Creator storefront; payout route needs country-specific review. | https://gumroad.com/help/article/13-getting-paid |
| Amazon Associates | Affiliate | Review program eligibility, local program and payout rules before applying. | https://affiliate-program.amazon.com/help/operating/policies |
| Clickworker | Microtasks | Registration and payout options can vary by country and workload. | https://support-workplace.clickworker.com/support/solutions/articles/80000671469-is-it-possible-to-work-for-clickworker-from-many-countries-all-over-the-world- |
| Prolific | Research studies | Participation is limited to supported countries and verification rules. | https://participant-help.prolific.com/en/articles/445007-who-can-participate-in-studies-on-prolific |

## Integration policy

- Candidate records start as `new`; no source is active and no credentials are stored.
- Human review must record the exact official terms/payout page, review date, explicit eligibility, payout method, currency and minimum payout.
- An approved source becomes a `pending` opportunity. It is activated separately only after review. Unknown country scope is never treated as global.
- Official API access is a separate gate from platform availability. Upwork documents OAuth 2.0 and developer-key review requirements. Do not promise an Upwork connector until access is actually granted.
- Manual-only platforms can still be tracked as opportunities; no scraping, browser-bot task completion, fake engagement, CAPTCHA bypass, or automated applications.
- Re-check terms before activation and after material provider changes.

## First-party API notes

Upwork API uses OAuth 2.0. API access requires an approved developer application and credentials. The developer documentation and legal terms define permitted use, rate limits and account obligations. Its help center describes API-key eligibility criteria including verified identity/payment details and a substantial lifetime earnings/spend threshold. Treat the API as unavailable until approval is received:
- https://support.upwork.com/hc/en-us/articles/115015857647-How-to-request-an-api-key-from-upwork
- https://support.upwork.com/hc/en-us/articles/115015933448-api-authentication-and-security
