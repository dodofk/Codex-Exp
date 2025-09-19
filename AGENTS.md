# Repository Guidelines

## Project Structure & Module Organization
Keep the root focused on `README.md`, `src/`, `tests/`, and `docs/`. Runtime assets belong in `src/assets/`; research artifacts live in `docs/research/`; working notes sit under `docs/notes/` with topical folders (`agents/`, `planning/`, `compliance/`, `datasets/`, `phases/`). Mirror source layout within `tests/`—`src/api/users.py` should pair with `tests/api/test_users.py`. Preserve `.code/agents/` transcripts until their outcomes are summarized in the appropriate notes subdirectory.

## Build, Test, and Development Commands
Rely on Make targets for repeatable workflows:
- `make init` installs toolchains, dependencies, and seeds `.env` templates.
- `make lint` runs formatters and static analysis in check mode; review diffs before escalating to `make lint-fix`.
- `make test` executes the full automated suite; run it before every commit or pull request.
Document any additional scripts inside `docs/notes/planning/` so the Director agent can schedule them in the roadmap.

### Dependency Management
- Use **uv** for all Python package operations (`uv pip install ...`, `uv pip sync ...`).
- Do **not** call `pip`/`python -m pip` directly—this repo standardizes on uv for reproducible environments.
- If a workflow requires new dependencies, add them to `pyproject.toml`, run `uv lock`, and note the change in the sprint backlog.

## Coding Style & Naming Conventions
`.editorconfig` enforces UTF-8, LF endings, 2-space indentation for docs, and 4-space indentation for code. Use snake_case for modules, kebab-case for configuration (`deployment-preview.yaml`), and PascalCase for class names. Run stack-appropriate formatters (`ruff --check`, `prettier --check`, `gofmt`) prior to commits; capture intentional deviations in an ADR within `docs/adr/`.

## Testing Guidelines
Default to `pytest` for Python surfaces and native harnesses elsewhere. Name tests `test_<feature>.py` or `<feature>.spec.ts`, target ≥80% coverage on critical flows, and collect fixtures under `tests/fixtures/`. Execute `make test` locally and include reproduction steps for any known flakes in `docs/notes/phases/evaluation-protocol.md` (once drafted) or sprint updates.

## Commit & Pull Request Guidelines
Follow Conventional Commit prefixes (`feat:`, `fix:`, `docs:`, etc.) and link issues in the footer (`Refs #123`). PRs must outline intent, validation steps, and supply screenshots or clips for UI changes. Confirm lint, tests, and relevant security scans pass before requesting review. Summaries of Phase deliverables should reference the roadmap and backlog docs to help the Director close checkpoints.

## Agent Collaboration Workflow
When delegating to agents, specify working directory, entry command, scope, and expected artifacts. Spawn specialized agents through the Director when work should be parallelized (e.g., multiple Data Scouts). Archive all agent outputs in `.code/agents/` with IDs, then summarize decisions in `docs/notes/agents/agent-briefs.md`, `docs/notes/planning/program-roadmap.md`, or `docs/notes/planning/sprint-backlog.md` before pruning raw transcripts.
