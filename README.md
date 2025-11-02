# OpenQueryBI-UI

Welcome to OpenQueryBI-UI — a lightweight demo UI and tooling around OpenQueryBI, a small toolkit for running AI-assisted SQL queries, validating SQL, and creating live plots backed by SQL. This repository contains a demo UI and server-side examples that show how to integrate the OpenQueryBI MCP tools and the FastAPI HTTP API.

This README documents the project, how the pieces fit together, how to run the demo locally or with Docker, configuration examples, API and MCP usage, development notes, and troubleshooting tips.

## Table of contents

- Project overview
- Repository layout
- Key components and contracts
- Requirements
- Quickstart (local)
- Quickstart (Docker)
- Configuration files (`databases.json`, `plot_info.json`)
- HTTP API reference (endpoints)
- MCP server tools and usage (SSE interface)
- Example workflows
- Development & contribution
- Security considerations
- Troubleshooting & FAQs
- Acknowledgements & license

## Project overview

OpenQueryBI-UI is a demo application showing how to use the OpenQueryBI toolset to:

- Expose a FastAPI HTTP API for database configuration, AI-backed SQL/plot requests, and fetching plot metadata.
- Run an MCP (Model Context Protocol) server that exposes tools such as `get_databases`, `validate_query`, and `plot_from_sql` via an SSE (Server-Sent Events) transport.
- Provide an example UI and helper services that showcase how a frontend can request AI-driven SQL and then validate or visualize results.

The included `servers/OpenQueryBI` directory contains a production-oriented MCP server and API implementation. The `client/` folder contains a smaller demo UI and helper code used by this repository to illustrate integration patterns.

This repository is intentionally small and focused — it is a reference/demo implementation rather than a production-ready platform. Use it as a starting point for building a secured, production system.

## Repository layout

Key files and folders (top-level):

- `client/` — demo client and small FastAPI app used by the UI (contains `app.py`, `config.py`, `apps/openquerybi_ui.py`, `services/`, `utils/`, and UI component code in `ui_components/`).
- `servers/OpenQueryBI/` — MCP server and full server-side implementation. Contains `main.py`, `api.py`, `ai.py`, and support files (see the `servers/OpenQueryBI/README.md` for more detail).
- `docker-compose.yaml`, `start.sh`, `requirements.txt` — orchestration and dependency manifest for running locally or in containers.
- `servers/OpenQueryBI/databases.json` (user-configurable) — database connection entries used by the MCP server.
- `servers/OpenQueryBI/plot_info.json` — persistent metadata for created plots.

Files of immediate interest:

- `client/app.py` — demo FastAPI app that demonstrates how to call `/ai/` and interact with the MCP tools.
- `servers/OpenQueryBI/api.py` — the HTTP API endpoints.
- `servers/OpenQueryBI/main.py` — MCP server implementation exposing tools to clients via SSE.
- `servers/OpenQueryBI/utils.py` — utilities used by the server (database management, ID generation, JSON persistence, etc.).

Refer to `servers/OpenQueryBI/README.md` (included in the repository) for deep-dive documentation about the MCP server internals.

## Key components and contracts

- FastAPI HTTP API (`servers/OpenQueryBI/api.py`): handles endpoints like `POST /databases/`, `POST /ai/`, `GET /plots/{plot_id}`.
- MCP server (`servers/OpenQueryBI/main.py`): exposes tools for the AI agent and clients (SSE transport by default) like `validate_query` and `plot_from_sql`.
- `databases.json`: JSON array with database definitions used to connect to SQL databases.
- `plot_info.json`: a map of `plot_id` -> metadata describing plots generated via `plot_from_sql`.

Minimal contracts:

- `databases.json` entry (example):

```
{
  "name": "analytics_pg",
  "description": "Production Postgres",
  "dialect": "postgresql",
  "config": {
    "host": "db.example.com",
    "port": 5432,
    "username": "user",
    "password": "pass",
    "database": "analytics",
    "sslmode": "require"
  }
}
```

- `plot_info.json` entry (example):

```
{
  "<plot_id>": {
    "type": "line",
    "database_configs": { /* copy of DB config used */ },
    "x": "timestamp",
    "y": "value",
    "query": "SELECT timestamp, value FROM series ORDER BY timestamp DESC",
    "limit": 100,
    "update_interval": 10,
    "title": "Graph requested to AI"
  }
}
```

The `plot_id` is generated deterministically via a hash of the plot payload so duplicates are avoided.

## Requirements

- Python 3.10+ recommended.
- The Python dependencies are listed in `requirements.txt` (root) and `servers/OpenQueryBI/requirements.txt` (server-specific). Typical packages include FastAPI, uvicorn, SQLAlchemy, pandas, and any DB driver you need (`psycopg2-binary` for PostgreSQL, built-in `sqlite3` for SQLite).
- Optional: Docker and docker-compose for containerized setup.

Install dependencies locally (example using pip):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r servers/OpenQueryBI/requirements.txt
```

Note: If you will connect to Postgres, install the required system-level packages (e.g., `libpq-dev`) or use the `psycopg2-binary` wheel.

## Quickstart — run locally

This section shows a minimal local run using the server code in `servers/OpenQueryBI` and the demo `client` application.

1. Ensure dependencies installed (see Requirements).
2. Configure local databases by editing `servers/OpenQueryBI/databases.json`. Use an array of database objects (see example earlier).
3. Start the MCP server and HTTP API (two approaches):

- Run MCP server directly (this hosts MCP tools for SSE):

```bash
cd servers/OpenQueryBI
python main.py
```

- Run the HTTP API (FastAPI) which uses the same tools via LangChain pipeline or local invocation (example uses uvicorn):

```bash
cd servers/OpenQueryBI
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

4. Start the demo client (optional) which demonstrates UI integration:

```bash
cd client
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

Now the HTTP API will be available at `http://localhost:8000` and the demo client at `http://localhost:8001` (if you run it as above).

## Quickstart — Docker

There is a `Dockerfile` for the server and `docker-compose.yaml` in the repo root for convenience.

Build and run a container:

```bash
docker compose build
docker compose up
```

This exposes the HTTP API and MCP server ports. Adjust mounts and ports to fit your environment.

## Configuration

- `servers/OpenQueryBI/databases.json`: list of database definitions (dialect + config). Keep credentials safe.
- `servers/OpenQueryBI/plot_info.json`: plot metadata store — auto-managed by `plot_from_sql`.

Make sure file permissions protect credentials when present. In production, consider moving secrets to environment variables or a secrets manager.

## HTTP API reference

Typical endpoints (implemented in `servers/OpenQueryBI/api.py`):

- POST `/databases/` — overwrite the databases config (body: JSON array of database entries). Server writes `databases.json` using `utils.save_databases_info`.
- GET `/plots/{plot_id}` — fetch plot metadata previously created by `plot_from_sql`.

Example: register databases with curl

```bash
curl -X POST http://localhost:8000/databases/ \
  -H "Content-Type: application/json" \
  -d @servers/OpenQueryBI/databases.json
```

Note: This UI/demo uses the MCP (Model Context Protocol) flow instead of an HTTP `/ai/` endpoint. The client (in `client/services/mcp_service.py`) implements a LangChain-compatible MCP client that connects to the OpenQueryBI MCP server via SSE and exposes tools to a local agent. See the "MCP & LangChain client in the UI" section below for details and usage patterns.
## MCP & LangChain client in the UI (no `/ai/` endpoint)

This demo UI uses the MCP (SSE) workflow exclusively and does not rely on an `/ai/` HTTP endpoint. Instead, the client implements a LangChain-style agent that connects directly to the OpenQueryBI MCP server. The relevant client code is in `client/services/mcp_service.py` and the prompt templates are in `client/utils/ai_prompts.py`.

Key points:

- `client/services/mcp_service.py` uses `MultiServerMCPClient` (from `langchain_mcp_adapters.client`) to open an MCP connection to the server(s) configured in the UI.
- The client creates an LLM instance (see `services/ai_service.py`) and uses `langgraph.prebuilt.create_react_agent` (or other LangChain agent builders) to wire the LLM with the set of MCP-provided tools returned by the MCP server.
- Tools available from the MCP server include `get_databases`, `validate_query`, `plot_from_sql`, and helpers (`get_tables`, `get_table_columns`). The agent executes tool calls as part of its reasoning flow.
- Prompts and behavioral rules are defined in `client/utils/ai_prompts.py`. The prompt enforces read-only SQL, limits attempts, and instructs the agent to call `validate_query` before any plotting step.

Usage pattern (high-level):

1. The UI starts and the user provides LLM parameters and server connection info.
2. The UI initializes a `MultiServerMCPClient` and retrieves the available tools from the MCP server.
3. The UI creates a LangChain/React-style agent with the LLM and the tools and then sends the user's query to the agent.
4. The agent calls `get_databases` to learn table shapes, generates a SQL query, validates it with `validate_query`, and — if requested — creates a plot via `plot_from_sql`.
5. `plot_from_sql` writes metadata to `servers/OpenQueryBI/plot_info.json` and returns a `plot_id` the UI can fetch with the HTTP API (`GET /plots/{plot_id}`).

Example: the UI initializes the MCP client and agent (see `client/services/mcp_service.py`):

- `MultiServerMCPClient` is used to connect to servers described in the UI `servers` configuration.
- After entering the LLM params the UI calls `connect_to_mcp_servers()` which:
  - creates the LLM
  - opens the MCP client
  - fetches tools with `client.get_tools()`
  - creates the agent via `create_react_agent(llm, tools)`

The UI then calls the agent via `agent.ainvoke({"messages": user_text})` (see `client/services/mcp_service.py`). Tool invocation is handled by the agent via the MCP tool wrappers.

You can find the concrete client example in `client/services/mcp_service.py` and the prompt templates in `client/utils/ai_prompts.py`.

## MCP server tools (SSE transport) — overview

The MCP server (in `servers/OpenQueryBI/main.py`) exposes several server-side tools intended for use by an agent or client connected via Server-Sent Events (SSE). Connect to `http://<host>:8002/sse` to use the MCP transport.

Main tools:

- `get_databases()` — returns a textual summary of configured databases for the AI or UI.

- `validate_query(database_name: str, query: str, limit: int = 100)` — Executes a SELECT query against the named database and returns a textual preview (pandas DataFrame string). Appends a `LIMIT` if missing for safety. Intended read-only; do not use for write queries.

- `plot_from_sql(type: str, database_name: str, query: str, x: str, y: str, limit: int = 100, update_interval: int = 10, title: str = "Graph requested to AI")` — Creates an entry in `plot_info.json` and returns a `plot_id`. Stores a copy of `database_configs` inside the plot info so the UI can request data later.

Helpers in `main.py`:

- `get_tables(database_name)` — list tables for database.
- `get_table_columns(database_name, table)` — column list for a table.

Security note: `validate_query` attempts to be read-only but there is no universal protection against malicious SQL. Ensure the DB user used has only the intended privileges.

## Example workflows

1) Validate a SQL query and then create a plot

- Call `validate_query('local_sqlite', 'SELECT timestamp, value FROM series ORDER BY timestamp DESC', limit=50)` via the MCP tool to preview results.
- If the result is correct, call `plot_from_sql('line', 'local_sqlite', 'SELECT timestamp, value FROM series ORDER BY timestamp DESC', 'timestamp', 'value', limit=50, update_interval=30)` to create the plot. The server saves an entry in `plot_info.json` and returns a `plot_id`.
- Use the HTTP API `GET /plots/<plot_id>` to fetch the plot metadata and render it in the frontend.

2) AI-driven flow using `/ai/`

- Client posts a natural language request to `POST /ai/`.
- The server runs the AI pipeline in `servers/OpenQueryBI/ai.py` which may internally call MCP tools (validate_query, plot_from_sql).
- The server returns a structured response describing actions taken and any created `plot_id`.

## Development & contribution

Repository conventions and tips:

- Follow Python typing and keep functions documented. Many server functions in `servers/OpenQueryBI` already provide docstrings.
- Add unit tests for utility functions in `servers/OpenQueryBI/utils.py` and tools in `servers/OpenQueryBI/main.py` when you add features.
- When changing any public behavior (API endpoints or data shapes), add or update tests under `servers/OpenQueryBI/test/`.

Suggested local dev workflow:

1. Create a feature branch: `git checkout -b feat/your-feature`.
2. Run tests and linters locally (if configured). Add tests for new behavior.
3. Open a PR and include a short description of changes and any migration notes.

Contribution notes

- Please avoid committing secrets (database passwords, API keys). Use environment variables or a `.env` local file excluded from VCS.
- If you add a new DB driver, document system-level install steps in the corresponding `servers/OpenQueryBI/README.md`.

## Security considerations

- Credentials: `databases.json` may contain credentials in plaintext. Keep it protected and avoid committing secrets.
- Principle of least privilege: use DB users limited to read-only for queries executed by the UI unless writes are required.
- CORS: the demo API config uses `allow_origins=["*"]`. In production, restrict origins to your frontend.
- Input sanitization: user-supplied SQL is executed by the server. Consider validating queries and/or using a read-only user.


## Example commands (quick reference)

Start FastAPI API (server folder):

```bash
cd servers/OpenQueryBI
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Start the demo client:

```bash
cd client
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

Register databases (curl):

```bash
curl -X POST http://localhost:8000/databases/ \
  -H "Content-Type: application/json" \
  -d @servers/OpenQueryBI/databases.json
```

Call AI endpoint (curl):

```bash
curl -X POST http://localhost:8000/ai/ \
  -H "Content-Type: application/json" \
  -d '{"query":"Create a line plot of user_signups over the last 30 days from analytics.users"}'
```

## Notes 
The demo uses some implementation choices for simplicity (e.g., storing `databases.json` and `plot_info.json` on disk). In production, you may want to move these to a secure store or database.
