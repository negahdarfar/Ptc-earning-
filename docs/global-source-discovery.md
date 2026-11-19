# Global source discovery catalogue

**Research snapshot:** 2026-11-20  
**Status:** 30 candidate leads only. This is not an endorsement, eligibility decision, payout guarantee, or permission to automate platform activity.

EarnOrbit seeds these providers into the persistent intake queue as `new` records. Every record starts with unknown country eligibility and unknown payout details. A human operator must inspect the provider's current official terms, supported residence countries, KYC/tax requirements, payment rails, minimum payout, fees, and task supply before approval. Approval creates a pending opportunity only; a separate activation step is required.

## Candidate portfolio

| Provider | Category | Official entry point | Research focus |
|---|---|---|---|
| Upwork | Client services | https://www.upwork.com/ | Contract fees, residence restrictions, withdrawal rails, API access |
| Fiverr | Client services | https://www.fiverr.com/ | Seller eligibility, payout methods, service fees |
| Contra | Client services | https://contra.com/ | Contractor eligibility, payment processing, fees |
| Freelancer.com | Client services | https://www.freelancer.com/ | Project fees, withdrawal minimums, identity checks |
| PeoplePerHour | Client services | https://www.peopleperhour.com/ | Seller onboarding, service fees, withdrawals |
| Toptal | Client services | https://www.toptal.com/ | Screening, contract terms, payment eligibility |
| 99designs | Client services | https://99designs.com/ | Designer fees, contest terms, payout methods |
| Gumroad | Digital products | https://gumroad.com/ | Creator onboarding, country-specific payout coverage |
| Etsy | Digital products | https://www.etsy.com/ | Etsy Payments availability, listing fees, digital-item policies |
| Ko-fi | Digital products | https://ko-fi.com/ | Payment processor coverage, fees, content rules |
| Patreon | Digital products | https://www.patreon.com/ | Creator eligibility, platform fees, payout and tax rules |
| Envato | Digital products | https://market.envato.com/ | Author applications, item review, revenue share |
| Creative Market | Digital products | https://creativemarket.com/ | Shop approval, licensing, fees, payouts |
| Adobe Stock Contributor | Digital products | https://contributor.stock.adobe.com/ | Contributor eligibility, licensing, tax and payout thresholds |
| Shutterstock Contributor | Digital products | https://submit.shutterstock.com/ | Contributor terms, content rights, payout methods |
| Freepik Contributor | Digital products | https://contributor.freepik.com/ | Contributor acceptance, licensing, revenue share |
| Amazon Associates | Affiliate | https://affiliate-program.amazon.com/ | Local program availability, traffic rules, payment thresholds |
| impact.com | Affiliate | https://impact.com/ | Advertiser approval, promotion rules, payment coverage |
| PartnerStack | Affiliate | https://partnerstack.com/ | Partner acceptance, program-specific terms, commissions |
| Awin | Affiliate | https://www.awin.com/ | Publisher approval, advertiser rules, payment thresholds |
| CJ Affiliate | Affiliate | https://www.cj.com/ | Publisher onboarding, advertiser rules, payout eligibility |
| Rakuten Advertising | Affiliate | https://rakutenadvertising.com/ | Publisher approval, market availability, payment details |
| Clickworker | Microtasks | https://www.clickworker.com/ | Registration country, task supply, available payment methods |
| TELUS Digital AI Community | Microtasks | https://www.telusdigital.com/careers/ai-community | Project-specific location, language and payment requirements |
| OneForma | Microtasks | https://www.oneforma.com/ | Project availability, qualification, country and payout options |
| Outlier | Microtasks | https://outlier.ai/ | Expert/project eligibility, task supply and payout terms |
| Prolific | Research | https://www.prolific.com/ | Supported participant countries, verification, cash-out |
| UserTesting | Research | https://www.usertesting.com/get-paid-to-test | Applicant eligibility, human testing and payout method |
| User Interviews | Research | https://www.userinterviews.com/ | Participant location, study screening, incentive delivery |
| Respondent | Research | https://www.respondent.io/ | Participant location, screening and incentive terms |

## Evidence rules

- Do not prefill any country as `GLOBAL`; unknown remains unknown.
- Do not infer eligibility from IP address, VPN, device location, nationality, or a payment wallet.
- Never falsify identity, residence, tax information, or payment details, and never bypass KYC or geographic restrictions.
- Do not automate account creation, applications, clicks, impressions, surveys, reviews, research participation, or task submissions unless the provider explicitly authorizes the exact automation.
- Only official APIs or expressly permitted partner feeds may be used for provider synchronization. Public-source monitoring, reminders, calculations, and ledger reconciliation may be automated.
- Keep pending rewards, approved task value, provider balances, and cash actually received as separate financial states.
- Re-check official terms immediately before activation and at least every 90 days thereafter. Stale evidence blocks activation.
- The USD 1,000 monthly objective is aspirational, not guaranteed. Focus on measured net cash per real hour rather than advertised headline rates.

## Current implementation boundary

The seed process only inserts missing research leads and never overwrites existing review decisions. No provider account is created, no credentials are collected, no external provider API is called, and no earning or payout is simulated. The queue is useful for prioritizing manual research; it is not a live integration.
