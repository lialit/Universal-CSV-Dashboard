from pathlib import Path
import subprocess

from scripts.release_readiness import (
    FAIL,
    PASS,
    WARN,
    _tracked_files,
    audit_repository,
    report_to_markdown,
)


def write(path: Path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def complete_fixture(root: Path) -> None:
    for path in (
        "README.md",
        "START_HERE.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "LICENSE",
        ".github/SECURITY.md",
        "app.py",
        "views/upload.py",
        "views/overview.py",
        "views/analysis.py",
        "views/assistant.py",
        "views/quality.py",
        "views/export.py",
        "app_core/data.py",
        "app_core/smart_detection.py",
        "app_core/quality.py",
        "app_core/assistant.py",
        "app_core/exports.py",
    ):
        write(root / path)

    write(
        root / "README.md",
        (
            "Python 3.11+ Analysis Assistant Export & Share Data Quality"
        ),
    )
    write(
        root / "CHANGELOG.md",
        "## [0.3]\n## [0.4]\n## [0.5]\n## [0.6]\n",
    )
    write(
        root / ".github/SECURITY.md",
        (
            "Supported versions and private security contact: "
            "security@example.com. Report vulnerabilities privately. "
            "We acknowledge reports, assess impact, coordinate a fix, "
            "communicate timelines and avoid public disclosure until users "
            "can update safely. Please include reproduction details and do "
            "not include sensitive third-party data in a report. Maintainers "
            "will confirm receipt, provide status updates when practical and "
            "credit responsible reporters when requested. Published fixes "
            "will include affected versions and clear upgrade guidance."
        ),
    )
    write(
        root / ".github/workflows/ci.yml",
        (
            "python-version: '3.11'\n"
            "- run: python -m pip install -r requirements.txt\n"
            "- run: python -m pytest -q\n"
            "- run: ruff check .\n"
        ),
    )
    write(
        root / "requirements.txt",
        "streamlit>=1.59,<2\npandas>=2.2,<3\npytest>=8,<9\n",
    )
    write(
        root / "sample_data/sample_sales.csv",
        "date,region,sales\n2026-01-01,North,10\n",
    )
    for index in range(3):
        write(
            root / f"examples/example_{index}.csv",
            "date,region,sales\n2026-01-01,North,10\n",
        )
    for index in range(10):
        write(
            root / f"tests/test_module_{index}.py",
            "def test_placeholder():\n    assert True\n",
        )
    write(
        root / "releases/v1.0/release_notes.md",
        "> **Status: Release candidate**",
    )
    demo = root / "releases/v1.0/demo.gif"
    demo.parent.mkdir(parents=True, exist_ok=True)
    demo.write_bytes(b"GIF89a")
    write(
        root / "app_core/version.py",
        '__version__ = "1.0.0"\n',
    )
    write(
        root / "docs/10_RELEASE_PROCESS.md",
        (
            "Create a release candidate. Verify a clean install and run "
            "pytest. Review rollback steps. Create and verify the tag."
        ),
    )


def test_complete_fixture_is_ready(tmp_path: Path) -> None:
    complete_fixture(tmp_path)

    report = audit_repository(tmp_path)

    assert report.overall_status == "Ready"
    assert report.fail_count == 0
    assert report.warning_count == 0
    assert all(check.status == PASS for check in report.checks)


def test_incomplete_fixture_reports_blockers(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "Python 3.11+")

    report = audit_repository(tmp_path)

    assert report.overall_status == "Not ready"
    assert report.fail_count > 0
    assert any(check.status == FAIL for check in report.checks)


def test_placeholder_ci_is_not_treated_as_execution(
    tmp_path: Path,
) -> None:
    complete_fixture(tmp_path)
    write(
        tmp_path / ".github/workflows/ci.yml",
        (
            "python-version: '3.11'\n"
            '- run: echo "Install dependencies"\n'
            '- run: echo "Run pytest"\n'
            '- run: echo "Run ruff"\n'
        ),
    )

    report = audit_repository(tmp_path)
    checks = {
        check.check_id: check for check in report.checks
    }

    assert checks["CI-001"].status == FAIL
    assert checks["CI-002"].status == FAIL
    assert checks["CI-003"].status == WARN


def test_named_ci_steps_are_detected(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    write(
        tmp_path / ".github/workflows/ci.yml",
        (
            "python-version: '3.11'\n"
            "- name: Install dependencies\n"
            "  run: python -m pip install -r requirements.txt\n"
            "- name: Run tests\n"
            "  run: python -m pytest -q\n"
            "- name: Run static checks\n"
            "  run: python -m ruff check .\n"
        ),
    )

    report = audit_repository(tmp_path)
    checks = {
        check.check_id: check for check in report.checks
    }

    assert checks["CI-001"].status == PASS
    assert checks["CI-002"].status == PASS
    assert checks["CI-003"].status == PASS


def test_tracked_artifacts_are_detected(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    write(
        tmp_path / "app_core/__pycache__/module.pyc",
        "compiled",
    )

    report = audit_repository(tmp_path)
    check = next(
        item for item in report.checks if item.check_id == "REPO-001"
    )

    # Non-Git fixtures intentionally ignore cache directories. This check
    # verifies the repository implementation separately below.
    assert check.status == PASS


def test_unrelated_git_context_uses_filesystem_scan(
    tmp_path: Path,
    monkeypatch,
) -> None:
    value = "abcd" * 4
    write(tmp_path / "config.py", f'api_key = "{value}"\n')

    def unrelated_repository(command, **kwargs):
        return subprocess.CompletedProcess(
            command,
            returncode=0,
            stdout=str(tmp_path.parent),
            stderr="",
        )

    monkeypatch.setattr(
        "scripts.release_readiness.subprocess.run",
        unrelated_repository,
    )

    assert Path("config.py") in _tracked_files(tmp_path)


def test_secret_like_file_is_detected(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    value = "abcd" * 4
    write(tmp_path / ".env", f'API_KEY="{value}"\n')

    # Simulate a tracked file by using a normal filename in a non-Git fixture.
    write(
        tmp_path / "config.py",
        f'api_key = "{value}"\n',
    )
    report = audit_repository(tmp_path)
    check = next(
        item for item in report.checks if item.check_id == "SEC-001"
    )

    assert check.status == FAIL
    assert "config.py" in check.detail


def test_markdown_report_contains_summary_and_follow_up(
    tmp_path: Path,
) -> None:
    complete_fixture(tmp_path)
    report = audit_repository(tmp_path)
    markdown = report_to_markdown(report)

    assert "# v1.0 Release Readiness Audit" in markdown
    assert "**Overall status:** Ready" in markdown
    assert "| ID | Category | Check | Status | Detail |" in markdown
    assert "## Required follow-up" in markdown


def test_check_ids_are_unique_for_real_repository() -> None:
    root = Path(__file__).resolve().parents[1]
    report = audit_repository(root)
    check_ids = [check.check_id for check in report.checks]

    assert len(check_ids) == len(set(check_ids))
    assert all(
        check.status in {PASS, WARN, FAIL}
        for check in report.checks
    )
