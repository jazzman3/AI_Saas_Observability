# Five Client-Focused AI Portfolio Projects

Independent, runnable, MIT-licensed demonstration applications. Each subdirectory is intended to become **its own public GitHub repository**. The builds are local MVP demos with automated tests—not claims of cloud deployment, customer adoption, or production security.

| Project | Business problem | Demo evidence |
|---|---|---|
| 01 Private Knowledge RAG | Document search with defensible citations | Grounded snippets, abstention, retrieval evaluation |
| 02 Agentic Lead Operations | Lead research to outreach and CRM handoff | Tool pipeline, checkpoints, approval gate, idempotent CRM |
| 03 AI Receptionist | Missed inbound leads and scheduling friction | Chat intent, leads, UTC slots, booking conflict test |
| 04 Document Intelligence | Manual invoice rekeying and bad data | Invoice extraction, schema rejection, review and CSV |
| 05 AI Operations Console | LLM app with no product telemetry | Web UI, API-key auth, cost/latency, regression harness |

## Start here
For each folder, `python -m venv .venv`, activate it, `pip install -r requirements.txt`, `pytest -q`, then `uvicorn app:app --reload`. Open `http://localhost:8000/docs` (project 05 also serves a frontend at `/`). Use **one server at a time** or assign ports 8001–8005.

## Public claims policy
- No live URLs, Loom links, client pilots or measured performance data are claimed as existing.
- `OPENAI_API_KEY` is optional. In its absence, demos use explicitly labeled simplified logic.
- Do **not** upload sensitive client documents, personal lead information, or real credentials to public demos.
- Do not claim real CRM, calendar, SMS or email integration where a mock/queue is provided.

## GitHub publication checklist
1. Create 5 GitHub repositories using the suggested folder names; initialize from each folder separately.
2. Run and capture your local unit tests, API screenshots and sample results; record date, environment and test sample sizes.
3. Add screenshots to `docs/`, your own 60–90-second Loom URL, and a real deployed demo link after deployment.
4. Add release/version tags, optional CI build, security controls, and measured benchmarks before describing anything as production-grade.
5. Add repository URLs to your resume only after pushing code and verifying the links.

See `RESUME_AND_CLIENT_SHOWCASE.md` for concise honest bullets, demo scripts and measurement plans.

