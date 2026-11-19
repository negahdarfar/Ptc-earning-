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

- GET /opportunities — list opportunities
- POST /opportunities — add an opportunity
- GET /revenue — revenue ledger
- POST /revenue — record revenue
- GET /summary — totals by currency

## Tests
    pip install pytest httpx
    pytest

## Opportunity discovery
The recommendation endpoint is deliberately conservative: an item must be marked active, have verified current terms, and use an official API. A country-specific query accepts only an explicit country code or `GLOBAL`; unknown eligibility is excluded. The ranking is a review-priority score, not an earnings forecast. See `docs/opportunity-review-policy.md` before approving a connector.

## Operator country profile

The initial operator profile is Iran (`IR`) for both residence and identity verification, as explicitly provided by the operator. Review opportunities with `country=IR`; never infer eligibility from IP location or crypto payout support. Unknown or unverified eligibility remains pending and is excluded from recommendations. See [docs/iran-eligibility-policy.md](docs/iran-eligibility-policy.md) for mandatory review rules and examples of restricted services.

## Safety and security
- Never commit private keys, passwords, API tokens, or wallet seed phrases.
- Keep secrets in environment variables or an ignored local .env file.
- Production refuses to start without EARNORBIT_API_TOKEN.
- Use HTTPS before exposing the service to the internet.
- This MVP records crypto payout information; it does not custody funds or sign transactions.
- Verify each platform's current terms and country restrictions before connecting it.

## License
MIT
