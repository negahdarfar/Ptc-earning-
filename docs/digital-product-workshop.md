# Digital product workshop

The product catalog is the first stage of the creator workflow. It stores product metadata and tracks whether a draft is ready for a later, separately reviewed publishing integration.

## Current capabilities

- Create and list digital product records through authenticated API endpoints.
- Store title, category, language, descriptions, asking price/currency, and an optional asset URL.
- Keep products in `draft`, `ready`, or `archived` state.
- Require an explicit rights confirmation and an asset URL before a product can be marked `ready`.
- All records are persisted in the existing SQLModel database.

## API

All routes require the EarnOrbit Bearer token.

- `POST /products` — create a product.
- `GET /products` — list all products.
- `GET /products?status=draft` — filter by status.

Example draft:

```json
{
  "title": "Original Trading Journal",
  "category": "template",
  "language": "en",
  "short_description": "A practical journal for reviewing trades.",
  "full_description": "An editable spreadsheet and usage guide.",
  "price_amount": "9.99",
  "price_currency": "USD",
  "status": "draft",
  "rights_confirmed": false
}
```

## Deliberate limitations

This is a catalog, not a storefront. It does not upload or host files, process customer payments, publish listings to marketplaces, or automatically deliver purchased files. An asset URL is metadata only; use a secure storage and delivery design before handling paid downloads.

A product marked `ready` only means its owner has confirmed the rights and supplied an asset URL. It does not mean that a marketplace, payment provider, country eligibility, sanctions review, or payout route has been approved.

Before any marketplace integration is enabled, record first-party evidence for seller-country eligibility, accepted identity documents, payout destination, supported currency, fees, refund rules, and API permissions. For the operator profile, evaluate Iran (`IR`) explicitly. If any requirement is unclear, keep the integration pending.
