----
id: 0002
title: Add `spec:lint` CLI command to validate OpenSpec project and proposals
authors: ["automated-assistant <assistant@example>"]
status: draft
created: 2025-11-03
----

# Summary

Add a new CLI command (e.g., `openspec spec:lint` or `openspec lint`) that validates OpenSpec project metadata (`openspec/project.md`) and proposal files in `openspec/proposals/`. The command helps ensure proposals follow the repository conventions and can be used in CI to block malformed proposals.

# Motivation

Currently there is no automated check enforcing proposal format, required fields, or common mistakes in `project.md`. A `spec:lint` command will:

- Catch missing metadata (missing status, missing acceptance criteria).
- Enforce proposal numbering and filename patterns.
- Provide clear, actionable errors for contributors and CI pipelines.

# Specification

CLI: `openspec spec:lint` or `openspec lint`

Behavior:

- Scan `openspec/project.md` and confirm required fields exist (project name, maintainers, tech stack).
- Scan `openspec/proposals/*.md` and for each file:
  - Validate YAML frontmatter contains `id`, `title`, `authors`, `status` and `created`.
  - Ensure filename starts with the zero-padded id (e.g., `0002-...`).
  - Ensure `status` is one of `draft`, `review`, `accepted`, `rejected`.
  - Check presence of essential sections: motivation, specification, acceptance criteria.
- Return exit code 0 on success; non-zero on validation errors and print human-friendly messages.

# Acceptance criteria

- The command exists and runs locally.
- It finds common errors in sample malformed proposal files (unit tests provided).
- It is runnable from CI (documented in README or project.md).

# Backwards compatibility

This is an additive feature and does not change existing proposal files. It only adds validation.

# Implementation plan

1. Add a small Node.js module (e.g., `bin/spec-lint.js`) that reads and validates files.
2. Add a `spec:lint` script to `package.json` or register a subcommand in the `openspec` CLI plugin if extending `@fission-ai/openspec` is desired.
3. Add unit tests validating both correct and malformed proposals.
4. Add a CI job that runs the lint on PRs touching `openspec/**`.

# Timeline

Estimate: 1-2 days for a minimal implementation (checker + tests); 3-5 days if integrating deeply into the `openspec` CLI and publishing a package.

# Risks

- False positives: initial rule set may flag acceptable proposals. Mitigation: start with a conservative rule set and iterate.

# Alternatives considered

- Relying on generic YAML/Markdown linters — they won't enforce OpenSpec-specific fields or proposal numbering.

# Implementation notes

The assistant can scaffold the checker and tests; maintainers must review and merge the PR. If you want, I can implement a minimal checker now and create the implementation branch locally for review.
