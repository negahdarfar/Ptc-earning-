# EarnOrbit
### Global Autonomous Crypto Earning Network

EarnOrbit is an open-source, modular platform for discovering and tracking legitimate online earning opportunities, managing affiliate/offerwall integrations, and recording verified revenue. It is designed to run on low-cost infrastructure and does not require a paid AI API or Ollama.

> **Important:** EarnOrbit does not generate guaranteed income. Each platform has its own eligibility, country, identity-verification, payout, and API rules. Use only official APIs and explicitly permitted integrations. No fake clicks, automated ad views, CAPTCHA bypass, or traffic manipulation.

## MVP status
- [x] FastAPI service
- [x] SQLite persistence
- [x] Opportunity registry and filtering
- [x] Revenue ledger and profit summary
- [x] API key-free local development
- [x] Docker deployment
- [ ] Verified platform connectors
- [ ] User authentication and multi-user permissions
- [ ] Payout integrations (official APIs only)

## Quick start
```bash
docker compose up --build
```
Open:
- API: http://localhost:8000
- Dashboard: http://localhost:8000/dashboard
- Interactive API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

Without Docker:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Core API
- `GET /health` — service status
- `GET /opportunities` — list opportunities
- `POST /opportunities` — add an opportunity
- `GET /revenue` — revenue ledger
- `POST /revenue` — record confirmed revenue
- `GET /summary` — totals and net profit

All monetary values are stored as decimal strings and include a currency code. Revenue records should represent actual confirmed amounts, not projections.

## Architecture
```
app/
  main.py          FastAPI routes
  database.py      SQLite setup
  models.py        SQLModel tables
  schemas.py       API validation
  services.py      business logic
```

## Safety and security
- Never commit private keys, passwords, API tokens, or wallet seed phrases.
- Keep secrets in environment variables.
- This MVP records crypto payout information; it does not custody funds or sign transactions.
- Enable authentication and HTTPS before exposing the service publicly.
- Verify each platform's current terms and country restrictions before connecting it.

## License
MIT
