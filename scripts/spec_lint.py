"""Simple OpenSpec linter for project.md and proposal files.

Checks performed:
- `openspec/project.md` contains required headings: Project name, Maintainers, Tech stack
- `openspec/proposals/*.md` frontmatter contains required keys: id, title, authors, status, created
- Proposal filenames start with zero-padded id
- Proposal status is one of allowed values (draft, review, accepted, rejected)
- Proposal body contains required sections: motivation, specification, acceptance criteria

Exit code: 0 = success (no errors), 1 = one or more errors found
"""
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).parent.parent
OPENSPEC_DIR = ROOT / "openspec"
PROPOSALS_DIR = OPENSPEC_DIR / "proposals"
PROJECT_MD = OPENSPEC_DIR / "project.md"

REQUIRED_PROPOSAL_KEYS = {"id", "title", "authors", "status", "created"}
ALLOWED_STATUS = {"draft", "review", "accepted", "rejected"}
REQUIRED_SECTIONS = ["motivation", "specification", "acceptance criteria"]


class LintError:
    def __init__(self, path: Path, message: str):
        self.path = path
        self.message = message

    def __str__(self):
        return f"{self.path}: {self.message}"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_project_md(path: Path):
    errors = []
    text = read_file(path)
    # Simple heading checks
    required_headings = ["## Project name", "## Maintainers", "## Tech stack"]
    for h in required_headings:
        if h not in text:
            errors.append(LintError(path, f"Missing heading: '{h}'"))
    return errors


def parse_frontmatter(text: str):
    # Try multiple frontmatter delimiters and handle CRLF or LF line endings.
    # Allow frontmatter to appear anywhere (be tolerant to BOM or stray chars at file start)
    patterns = [r"----\r?\n(.*?)\r?\n----\r?\n", r"---\r?\n(.*?)\r?\n---\r?\n"]
    for pat in patterns:
        m = re.search(pat, text, flags=re.S | re.M)
        if m:
            fm_text = m.group(1)
            body = text[m.end() :]
            try:
                fm = yaml.safe_load(fm_text)
            except Exception:
                return None, text
            return fm or {}, body
    return None, text


def validate_proposal(path: Path):
    errors = []
    text = read_file(path)
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append(LintError(path, "Missing or invalid YAML frontmatter (---- ... ----)"))
        return errors

    # keys
    missing = REQUIRED_PROPOSAL_KEYS - set(fm.keys())
    if missing:
        errors.append(LintError(path, f"Missing frontmatter keys: {sorted(list(missing))}"))

    # filename check: filename should start with id
    fid = str(fm.get("id", "")).zfill(4)
    fname = path.name
    if not fname.startswith(fid):
        errors.append(LintError(path, f"Filename does not start with zero-padded id '{fid}'"))

    # status check
    status = str(fm.get("status", "")).lower()
    if status not in ALLOWED_STATUS:
        errors.append(LintError(path, f"Invalid status '{status}'. Allowed: {sorted(ALLOWED_STATUS)}"))

    # body section checks (case-insensitive)
    body_lower = body.lower()
    for section in REQUIRED_SECTIONS:
        if section not in body_lower:
            errors.append(LintError(path, f"Missing required section: '{section}'"))

    return errors


def run_lint():
    all_errors = []
    # project.md
    if not PROJECT_MD.exists():
        all_errors.append(LintError(PROJECT_MD, "Missing file"))
    else:
        all_errors.extend(validate_project_md(PROJECT_MD))

    # proposals
    if not PROPOSALS_DIR.exists():
        all_errors.append(LintError(PROPOSALS_DIR, "Missing proposals directory"))
    else:
        md_files = sorted(PROPOSALS_DIR.glob("*.md"))
        for p in md_files:
            all_errors.extend(validate_proposal(p))

    if all_errors:
        print("Spec lint found issues:\n")
        for e in all_errors:
            print(f"- {e}")
        return 1

    print("Spec lint: no issues found.")
    return 0


if __name__ == "__main__":
    rc = run_lint()
    sys.exit(rc)
