from pathlib import Path

from scripts.security_review import (
    FAIL,
    PASS,
    audit_security,
    review_to_markdown,
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def complete_fixture(root: Path) -> None:
    write(
        root / "views/upload.py",
        "payload = uploaded_file.getvalue()\n",
    )
    write(
        root / "app_core/data.py",
        "from io import BytesIO\nbuffer = BytesIO(file_bytes)\n",
    )
    write(root / "app.py", "print('local runtime')\n")
    write(
        root / ".streamlit/config.toml",
        '[client]\nshowErrorDetails = "none"\n',
    )
    write(
        root / "docs/12_SECURITY_PRIVACY.md",
        (
            "local-first temporary session state external processing "
            "Excel security "
        )
        * 70,
    )
    write(
        root / "requirements.txt",
        "streamlit>=1.59,<2\n",
    )
    write(
        root / "requirements-security.txt",
        "pip-audit>=2.9,<3\n",
    )
    write(
        root / ".github/workflows/ci.yml",
        (
            "run: python -m pip_audit -r requirements.txt --strict\n"
        ),
    )


def checks_by_id(root: Path):
    return {
        check.check_id: check
        for check in audit_security(root).checks
    }


def test_complete_fixture_passes(tmp_path: Path) -> None:
    complete_fixture(tmp_path)

    review = audit_security(tmp_path)

    assert review.passed
    assert all(check.status == PASS for check in review.checks)


def test_external_runtime_client_fails(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    write(tmp_path / "app_core/client.py", "import requests\n")

    check = checks_by_id(tmp_path)["PRIV-002"]

    assert check.status == FAIL
    assert "requests" in check.detail


def test_framework_independent_csv_parser_passes(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    write(
        tmp_path / "app_core/data.py",
        "from app_core.csv_parser import parse_csv_bytes\n",
    )
    write(
        tmp_path / "app_core/csv_parser.py",
        "from io import BytesIO\nbuffer = BytesIO(file_bytes)\n",
    )

    check = checks_by_id(tmp_path)["PRIV-001"]

    assert check.status == PASS


def test_public_error_details_fail(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    write(
        tmp_path / ".streamlit/config.toml",
        '[client]\nshowErrorDetails = "full"\n',
    )

    check = checks_by_id(tmp_path)["PRIV-003"]

    assert check.status == FAIL


def test_missing_dependency_gate_fails(tmp_path: Path) -> None:
    complete_fixture(tmp_path)
    write(tmp_path / "requirements-security.txt", "")

    check = checks_by_id(tmp_path)["DEP-SEC-001"]

    assert check.status == FAIL


def test_markdown_contains_every_control(tmp_path: Path) -> None:
    complete_fixture(tmp_path)

    markdown = review_to_markdown(audit_security(tmp_path))

    assert "**Overall status:** PASS" in markdown
    assert "PRIV-001" in markdown
    assert "DEP-SEC-001" in markdown


def test_real_repository_passes_security_review() -> None:
    root = Path(__file__).resolve().parents[1]

    assert audit_security(root).passed
