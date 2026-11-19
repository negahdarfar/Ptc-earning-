# EarnOrbit
### Global Autonomous Crypto Earning Network

EarnOrbit is an open-source, modular platform for discovering and tracking legitimate online earning opportunities, managing affiliate/offerwall integrations, and recording verified revenue. It is designed to run on low-cost infrastructure and does not require a paid AI API or Ollama.

> **Important:** EarnOrbit does not generate guaranteed income. Each platform has its own eligibility, country, identity-verification, payout, and API rules. Use only official APIs and explicitly permitted integrations. No fake clicks, automated ad views, CAPTCHA bypass, or traffic manipulation.

## MVP status
- [x] FastAPI service and SQLite persistence
- [x] Opportunity registry and revenue ledger
- [x] Revenue summary and responsive dashboard
- [x] Bearer-token protection for private API endpoints
- [x] Production startup fails closed if the API token is missing
- [x] Docker Compose requires an externally supplied API token
- [x] Authenticated digital product catalog (draft/ready/archived)
- [x] Reviewed global opportunity catalog for manual and API-enabled sources
- [ ] Secure file storage and delivery
- [ ] Verified platform connectors
- [ ] Multi-user accounts and role-based permissions
- [ ] Payout integrations (official APIs only)

## Secure Docker start
Create a local .env file (it is gitignored) containing a long random secret:

    EARNORBIT_API_TOKEN=replace-with-a-long-random-secret

Then run:

    docker compose up --build -d

Open the dashboard at http://localhost:8000/dashboard, API docs at http://localhost:8000/docs, and health check at http://localhost:8000/health.

Enter the same token in the dashboard API access section. The browser stores it in session storage for the current tab only. Do not use plain HTTP over an untrusted network; put the service behind HTTPS before remote access.

## Local development
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    export EARNORBIT_API_TOKEN='your-long-random-local-secret'
    uvicorn app.main:app --reload

## Core API
All endpoints except GET / and GET /health require the Authorization header in this format:

    Authorization: Bearer YOUR_EARNORBIT_API_TOKEN

- GET /opportunities — list opportunities (optional `category` and `status` filters)
- GET /opportunities/catalog — reviewed active sources, including manual-only PTC/GPT sources (not an automation permission)
- POST /opportunities — add an opportunity
- GET /revenue — revenue ledger
- POST /revenue — record revenue
- GET /products — list digital products
- POST /products — create a digital product draft
- GET /summary — totals by currency

## Tests
    pip install pytest httpx
    pytest

## Global PTC and reward-source discovery
EarnOrbit can catalog worldwide source categories such as `ptc`, `gpt`, `offerwall`, `microtask`, `survey`, `affiliate`, and `crypto_rewards`. Use `GET /opportunities/catalog?category=ptc` to view active entries whose terms have been reviewed. This catalog supports manual-only sites even when they do not publish an official API. A catalog entry is not proof of earnings, global eligibility, or permission to automate activity. Respect each provider's current rules; ad views, clicks, surveys, and tasks may only be automated where the provider explicitly authorizes it. Never simulate human engagement.

## Opportunity discovery
The recommendation endpoint is deliberately conservative: an item must be marked active, have verified current terms, and use an official API. A country-specific query accepts only an explicit country code or `GLOBAL`; unknown eligibility is excluded. The ranking is a review-priority score, not an earnings forecast. See `docs/opportunity-review-policy.md` before approving a connector.

## Privacy-conscious eligibility and connectors

The operator's personal residence, identity documents, and verification profile are not published in this repository. Each opportunity is evaluated against the provider's current official terms for the user's actual circumstances. Unknown or conflicting eligibility remains pending; never infer eligibility from IP, VPN, device location, or payout wallet.

The connector framework uses auditable manifests and an in-memory registry. Connectors are disabled by default. Enabling one requires an official HTTPS API, HTTPS terms URL, a dated terms review, a positive rate limit, and an explicit supported-country declaration. Runtime country filtering is applied only when the operator selects a country profile. Candidate data is untrusted and is never auto-approved. The framework contains no live platform adapters and makes no external network calls.

See [opportunity review policy](docs/opportunity-review-policy.md) and [profitability roadmap](docs/profitability-roadmap.md).

## Digital product workshop

The first creator workflow is available through the authenticated `/products` API. It stores product metadata and validates draft/ready status, including rights confirmation before a product is marked ready. It does not upload files, host downloads, process payments, or publish to external marketplaces. See [docs/digital-product-workshop.md](docs/digital-product-workshop.md).

## Safety and security
- Never commit private keys, passwords, API tokens, or wallet seed phrases.
- Keep secrets in environment variables or an ignored local .env file.
- Production refuses to start without EARNORBIT_API_TOKEN.
- Use HTTPS before exposing the service to the internet.
- This MVP records crypto payout information; it does not custody funds or sign transactions.
- Verify each platform's current terms and country restrictions before connecting it.

## License
MIT
