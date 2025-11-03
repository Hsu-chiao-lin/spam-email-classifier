## OpenSpec workflow and agent roles

This file describes how humans and AI agents (including the assistant you are working with) collaborate using the OpenSpec repository layout in this project.

### Roles

- Maintainers: humans responsible for final approvals, merging PRs, and setting project strategy.
- Contributors: humans who author proposals and code changes.
- AI assistant: an automated agent that can draft proposals, apply edits, run local commands (when granted), update the todo list, and produce PR-ready changes. The AI does not merge changes or approve proposals.

### High-level workflow

1. Idea / Request
	- A contributor describes a desired change (feature, bugfix, or doc update).

2. Proposal
	- Create a proposal under `openspec/proposals/` using the next available number and a clear slug.
	- Set `status: draft` while iterating.
	- The proposal should include: motivation, specification, acceptance criteria, backward-compatibility notes, implementation plan, and timeline.

3. Review
	- Maintainers and contributors review the proposal. Feedback is addressed by updating the proposal file.

4. Acceptance
	- When reviewers agree, change the proposal status to `accepted` and open an implementation PR that references the proposal.

5. Implementation & tests
	- Implement the change in a feature branch, add tests, run CI, and open a PR.

6. Merge & release
	- Maintainers merge when CI passes and the PR satisfies the acceptance criteria. Update changelogs and create releases as needed.

### How to work with the AI assistant on this repo

1. Give the assistant a clear, concrete request (for example: "Create a proposal to add a `spec:lint` command that validates proposal format and `project.md` conventions").
2. The assistant will:
	- Add or update files in the repo (proposal drafts, project metadata).
	- Use the `todo` mechanism in the repository workspace to track progress.
	- Run local commands you allow (e.g., `npm install`, `openspec` CLI) and report output.
	- Propose PR content; you (or a maintainer) should open the PR and perform the merge/approval steps.
3. Review changes suggested by the assistant. If anything should be different, ask the assistant to revise the file(s) and iterate until you are satisfied.

### Safety & permissions

- The assistant can prepare changes and run commands in your workspace but will not push or merge without explicit instruction.
- For operations requiring elevated permissions (admin install, system changes), run those commands manually or explicitly grant the assistant permission to run them.

### Tips for smooth collaboration

- Provide small, testable requests and prefer incremental changes.
- When requesting proposals, include the acceptance criteria you expect.
- Keep the `openspec/proposals/` filenames and numbering tidy; the assistant can propose the next available number but confirm before finalizing.

If you'd like, I can keep this file as the canonical workflow and update it later as your team refines roles and processes.
