## Project name

openspec-demo

## Short description

This repository demonstrates using OpenSpec to manage change proposals and an agent-driven workflow for small projects. It includes the project metadata and a proposals folder where changes are proposed, reviewed, and accepted.

## Maintainers

- Name: Hsu-chiao-lin
- Email: <fill-in>
- GitHub: Hsu-chiao-lin

Replace the email placeholder above with the preferred contact address.

## Tech stack

- Primary runtime & package manager: Node.js (>=16) and npm for OpenSpec tooling
- Python environment (>=3.8) for ML components:
  - Scientific stack: scikit-learn, pandas, numpy
  - Development: pytest, jupyter notebooks
- CLI tooling: OpenSpec (`@fission-ai/openspec`) and standard Unix-like tooling (works on Windows via PowerShell)
- Editor: Visual Studio Code (recommended)
- Docs and proposals: Markdown
- Version control: Git (GitHub recommended)
- CI: GitHub Actions (recommended)

## Conventions

- Branch naming: feature/<short-desc>, fix/<short-desc>, chore/<short-desc>
- Commit messages: Use conventional commits style (type(scope): short-desc)
- Proposal files: all change proposals live in `openspec/proposals/` and are numbered with `0001-...`, `0002-...`.
- Proposal lifecycle: draft -> review -> accepted -> implemented
- PRs: link to the proposal file in the PR body and include the proposal number in the branch name (e.g., `proposal/0002-add-spec-lint`)

## Development setup

1. Install Node.js and npm.
2. (Optional) Install OpenSpec CLI globally:

	npm install -g @fission-ai/openspec@latest

3. Install local dev deps (if any):

	npm install

4. Run tests / linters if present. Add test commands to `package.json`.

## Proposal process (high level)

1. Create a proposal file in `openspec/proposals/` with the next available number and a short slug.
2. Mark the status as `draft` and request review from maintainers.
3. Iterate on feedback until ready; then change status to `accepted` (or have maintainers merge the proposal PR).
4. Implement the change in a feature branch that references the proposal.

## File layout

- `openspec/project.md` — this file, describing the project.
- `openspec/AGENTS.md` — workflow and roles for human and AI agents.
- `openspec/proposals/` — folder containing numbered proposal markdown files.

## Tests & CI

Add a `package.json` scripts section with at least `test`, `lint`, and `spec:check` (or `spec:lint`) commands. Add GitHub Actions to run tests and check proposals on PRs.

## License

Specify a license (e.g., MIT) here and add a `LICENSE` file.

## Notes

This project file is a starting point — replace placeholders (maintainers, contact info) and extend sections (detailed CI, test commands) to match your project specifics.
