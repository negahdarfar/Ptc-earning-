# Initial source intake catalogue

The application seeds these six records into the source intake queue as `new`. They are research leads only, not approved opportunities or eligibility claims.

| Source | Category | First-party starting point |
|---|---|---|
| Upwork | Client services | https://www.upwork.com/legal ; https://www.upwork.com/developer/documentation/graphql/api/docs/index.html |
| Fiverr | Productized services | https://www.fiverr.com/legal-portal/legal-terms/terms-of-service |
| Gumroad | Original digital products | https://gumroad.com/help/article/13-getting-paid |
| Amazon Associates | Affiliate | https://affiliate-program.amazon.com/help/operating/policies |
| Clickworker | Microtasks | https://support-workplace.clickworker.com/support/solutions/articles/80000671469-is-it-possible-to-work-for-clickworker-from-many-countries-all-over-the-world- |
| Prolific | Research studies | https://participant-help.prolific.com/en/articles/445007-who-can-participate-in-studies-on-prolific |

## Intake and activation policy

- The six records are inserted once at startup as `new`; no account is created, no connector is enabled, and no earnings are assumed.
- Human review must record the official terms/payout URL, review date, explicit eligibility, payout method, currency and minimum payout.
- An approved source becomes a `pending` opportunity. It is activated separately only after fresh evidence review. Unknown country scope is never treated as global.
- Official API access is a separate gate from platform availability. Upwork documents OAuth 2.0 and developer-key review requirements. Its current help page lists account-verification and lifetime activity criteria for API-key applications. Treat the API as unavailable until approval is received.
- Manual-only platforms can still be tracked as opportunities; no scraping, browser-bot task completion, fake engagement, CAPTCHA bypass, or automated applications.

## Upwork API sources

- API authentication and OAuth 2.0: https://support.upwork.com/hc/en-us/articles/115015933448-API-authentication-and-security
- API-key eligibility and application: https://support.upwork.com/hc/en-us/articles/115015857647-How-to-request-an-api-key-from-upwork
- Developer API documentation: https://www.upwork.com/developer/documentation/graphql/api/docs/index.html
