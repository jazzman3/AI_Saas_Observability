# AI Operations Console — authenticated full-stack app + telemetry

**Business problem:** LLM prototypes lack user accounts, deployment interfaces, cost visibility and basic regression tests. **Target outcome:** A small auditable AI web product that can be extended into a team-facing application.

## Shipped features
Responsive HTML/JS frontend, FastAPI JSON API, account creation with salted scrypt password hashes, random bearer tokens stored hashed in SQLite, per-user query records, LLM optional provider, per-query latency, provider token counts, configurable estimated price and p50/p95 request latency. A small evaluation regression script runs labeled prompts. Health route and Dockerfile included.

## Local run
```bash
pip install -r requirements.txt
uvicorn app:app --reload
pytest -q
python evaluate.py
```
Open `http://localhost:8000` to sign up, query and view metrics. By default the provider uses a clearly marked mock answer. To use OpenAI, set `OPENAI_API_KEY`, `OPENAI_MODEL`, and the *current* `INPUT_USD_PER_1M` and `OUTPUT_USD_PER_1M` for accurate estimated USD billing. Defaults are zero instead of a fictitious cost.

## Security and deployment notes
This is a runnable local product **not yet internet-production hardened**. Add login/token rotation, email verification, password reset, HTTPS, rate limiting, CSRF analysis for future cookie auth, secrets management, per-tenant RBAC, retention/deletion controls, centralized OpenTelemetry, structured error events, data migrations and a managed PostgreSQL database. The API uses the same origin as the UI. Do not upload actual client information in this demo.

## Evaluation + outcome narrative
Run `evaluate.py` only after starting the server. Its keyword coverage is a weak smoke test, **not factual accuracy**. Add human-graded correctness, prompt injection checks, toxicity/PII tests, model comparison and drift regression over versioned datasets. Showcase an end-to-end signup → LLM query → metrics flow, and report verified p50/p95, token usage and cost/request.
