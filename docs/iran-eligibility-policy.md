# Iran eligibility policy (IR)

**Default operating profile:** the operator has stated that their country of residence and identity-verification country are Iran (ISO 3166-1 alpha-2: `IR`).

## Mandatory rules

1. Treat `IR` as the operator country for opportunity review. Do not infer another residence from IP address, VPN, device location, payment wallet, or a third-party service.
2. Never recommend a platform merely because its website loads or it advertises crypto payouts.
3. Before an opportunity can become `active`, verify the platform's current primary-source terms for (a) Iran residence, (b) Iranian identity documents/KYC, (c) account creation and ongoing use, (d) payout eligibility, and (e) the specific payout rail.
4. If Iran is prohibited, or the terms explicitly exclude residents of Iran, mark the opportunity ineligible and do not suggest circumvention.
5. If the terms are silent, ambiguous, stale, or contradictory, keep eligibility `unknown` / status `pending`. Unknown is not approval and must not be treated as `GLOBAL`.
6. A crypto payout method does not override country restrictions, sanctions screening, KYC requirements, or wallet screening.
7. Do not use VPNs, false addresses, borrowed identities, nominee accounts, or other methods to evade restrictions.
8. Re-check primary-source terms before onboarding and periodically thereafter. Store the source URL, checked date, reviewer, and a short evidence note in the opportunity record.
9. Do not store identity documents, seed phrases, private keys, or exchange credentials in EarnOrbit or GitHub. The MVP only records payout references; it does not custody funds or sign transactions.

## Evidence examples (not an allowlist)

These currently published terms illustrate why country-by-country review is required:

- WhiteBIT's affiliate-program help page lists Iran among restricted/prohibited regions: https://help.whitebit.com/hc/en-gb/articles/21160598101149-How-to-use-the-WhiteBIT-Affiliate-Program-functionality
- Kraken's global terms exclude residents of sanctioned/embargoed jurisdictions, explicitly including Iran: https://www.kraken.com/legal/global-terms
- BitMEX's restricted-jurisdiction policy lists Iran as a sanctioned jurisdiction: https://www.bitmex.com/restricted-jurisdiction-policy/

These examples are not legal advice and are not a complete survey of services. Terms can change; always inspect the current primary source for the exact product and payout program.

## Current implementation boundary

The existing recommendation endpoint filters records based on manually stored country eligibility, verified terms, active status, and official API status. It does **not** independently crawl platforms, interpret legal terms, verify KYC acceptance, or prove that a payout will succeed. An operator must complete the evidence review before setting `terms_verified=true` and `status=active`.

For country-specific recommendations, query with `country=IR`. Records marked `unknown` are excluded.
