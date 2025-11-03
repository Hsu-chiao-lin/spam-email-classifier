----
id: 0001
title: Interactive project initialization
authors: ["automated-assistant <assistant@example>"]
status: draft
created: 2025-11-03
----

# Summary

Add interactive initialization to create new OpenSpec projects, automating the setup of the standard directory structure, initial `project.md`, and recommended configuration files.

# Motivation

Currently, users must manually create the OpenSpec directory structure and project metadata. An interactive initializer will:
- Reduce friction for new projects
- Ensure consistent project structure
- Pre-populate required fields with sensible defaults
- Set up recommended tooling (linters, CI)

# Specification

New command: `openspec init` or `openspec new`

Interactive prompts:
1. Project name
2. Short description
3. Maintainer info (name, email, GitHub)
4. License choice
5. Optional: initialize git repo
6. Optional: add GitHub Actions workflow

Generated files:
- `openspec/project.md` with user inputs
- `openspec/AGENTS.md` with standard workflow
- `openspec/proposals/` directory
- `.gitignore` with standard exclusions
- Optional: GitHub Actions workflow for proposal validation

# Acceptance criteria

- Command successfully creates new project structure
- Generated files are valid and follow conventions
- Interactive mode works on Windows and Unix
- Non-interactive mode supported with CLI flags
- Clear error messages on validation failures

# Backwards compatibility

This is an additive feature that only affects new project creation.

# Implementation plan

1. Add interactive prompts using a CLI framework
2. Create file templates with variables
3. Add validation for user inputs
4. Implement non-interactive mode
5. Add tests for file generation
6. Document in README

# Timeline

Estimate: 2-3 days for implementation and testing.

# Risks

- File permission issues in different environments
- Terminal compatibility for interactive mode
- Template maintenance as conventions evolve

# Notes

This provides the foundation for automated project setup that proposals 0002 and 0003 can build upon.