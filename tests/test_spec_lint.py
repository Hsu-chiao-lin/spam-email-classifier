from pathlib import Path
from scripts.spec_lint import validate_project_md, validate_proposal, PROJECT_MD, PROPOSALS_DIR


def test_project_md_exists_and_has_required_headings():
    assert PROJECT_MD.exists()
    errors = validate_project_md(PROJECT_MD)
    assert errors == []


def test_proposals_lint():
    assert PROPOSALS_DIR.exists()
    md_files = sorted(PROPOSALS_DIR.glob("*.md"))
    assert len(md_files) >= 1
    for p in md_files:
        errors = validate_proposal(p)
        # Allow some proposals to be drafts, but they should have frontmatter and required sections
        assert errors == [] , f"Lint errors for {p}: {errors}"
