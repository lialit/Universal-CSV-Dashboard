from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from typing import Iterable

try:
    from scripts.security_review import SecurityReview, audit_security
except ModuleNotFoundError:
    from security_review import SecurityReview, audit_security


PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"


@dataclass(frozen=True)
class ReadinessCheck:
    """One release-readiness requirement and its current result."""

    check_id: str
    category: str
    title: str
    status: str
    detail: str
    remediation: str


@dataclass(frozen=True)
class ReleaseReadinessReport:
    """Complete static readiness assessment for one repository state."""

    checks: tuple[ReadinessCheck, ...]

    @property
    def pass_count(self) -> int:
        return sum(check.status == PASS for check in self.checks)

    @property
    def warning_count(self) -> int:
        return sum(check.status == WARN for check in self.checks)

    @property
    def fail_count(self) -> int:
        return sum(check.status == FAIL for check in self.checks)

    @property
    def overall_status(self) -> str:
        if self.fail_count:
            return "Not ready"
        if self.warning_count:
            return "Needs review"
        return "Ready"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _check(
    check_id: str,
    category: str,
    title: str,
    status: str,
    detail: str,
    remediation: str = "",
) -> ReadinessCheck:
    return ReadinessCheck(
        check_id=check_id,
        category=category,
        title=title,
        status=status,
        detail=detail,
        remediation=remediation,
    )


def _scanned_files(root: Path) -> tuple[Path, ...]:
    excluded = {".git", ".venv", ".pytest_cache", "__pycache__"}
    return tuple(
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in excluded for part in path.parts)
    )


def _tracked_files(root: Path) -> tuple[Path, ...]:
    try:
        repository = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        repository_root = Path(repository.stdout.strip()).resolve()
        if repository_root != root.resolve():
            return _scanned_files(root)

        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return _scanned_files(root)

    return tuple(
        Path(value)
        for value in result.stdout.split("\0")
        if value
    )


def _actual_run_step(workflow: str, pattern: str) -> bool:
    expression = re.compile(pattern, flags=re.IGNORECASE)
    for line in workflow.splitlines():
        stripped = line.strip()
        if stripped.startswith("- run:"):
            command = stripped.removeprefix("- run:").strip()
        elif stripped.startswith("run:"):
            command = stripped.removeprefix("run:").strip()
        else:
            continue
        if command.lower().startswith("echo"):
            continue
        if expression.search(command):
            return True
    return False


def _bounded_requirements(requirements: str) -> tuple[bool, list[str]]:
    unbounded: list[str] = []
    for raw_line in requirements.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "<" not in line or ">=" not in line:
            unbounded.append(line)
    return not unbounded, unbounded


def _secret_findings(
    root: Path,
    tracked: Iterable[Path],
) -> list[str]:
    sensitive_names = {
        ".env",
        "secrets.toml",
        "id_rsa",
        "id_ed25519",
    }
    sensitive_suffixes = {
        ".pem",
        ".key",
        ".p12",
        ".pfx",
    }
    content_pattern = re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)"
        r"\s*[:=]\s*['\"][^'\"]{12,}['\"]"
    )
    findings: list[str] = []

    for relative in tracked:
        if (
            relative.name in sensitive_names
            or relative.suffix.lower() in sensitive_suffixes
        ):
            findings.append(str(relative))
            continue

        path = root / relative
        try:
            if path.stat().st_size > 1_000_000:
                continue
        except OSError:
            continue
        text = _read(path)
        if text and content_pattern.search(text):
            findings.append(f"{relative} (credential-like value)")

    return findings


def _required_documentation_check(root: Path) -> ReadinessCheck:
    required = (
        "README.md",
        "START_HERE.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "LICENSE",
        ".github/SECURITY.md",
    )
    missing = [
        path for path in required if not (root / path).is_file()
    ]
    return _check(
        "DOC-001",
        "Documentation",
        "Required public documents",
        FAIL if missing else PASS,
        (
            "Missing: " + ", ".join(missing)
            if missing
            else "README, onboarding, changelog, contribution, license and "
            "security documents are present."
        ),
        "Add every missing public document." if missing else "",
    )


def _application_structure_check(root: Path) -> ReadinessCheck:
    required = (
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
    )
    missing = [
        path for path in required if not (root / path).is_file()
    ]
    return _check(
        "APP-001",
        "Product",
        "Core application structure",
        FAIL if missing else PASS,
        (
            "Missing: " + ", ".join(missing)
            if missing
            else "All core pages and analytical modules are present."
        ),
        "Restore the missing runtime files." if missing else "",
    )


def _sample_data_check(root: Path) -> ReadinessCheck:
    path = root / "sample_data/sample_sales.csv"
    text = _read(path)
    header = text.splitlines()[0] if text else ""
    required_columns = {
        "date",
        "region",
        "sales",
    }
    columns = {
        value.strip() for value in header.split(",") if value.strip()
    }
    valid = path.is_file() and required_columns.issubset(columns)
    return _check(
        "DATA-001",
        "Product",
        "Safe representative sample",
        PASS if valid else FAIL,
        (
            "sample_sales.csv contains the minimum supported demo fields."
            if valid
            else "The demo CSV is missing or lacks date, region or sales."
        ),
        "Provide a non-sensitive sample CSV with supported fields." if not valid else "",
    )


def _example_coverage_check(root: Path) -> ReadinessCheck:
    examples = list((root / "examples").glob("*.csv"))
    valid = len(examples) >= 3
    return _check(
        "DATA-002",
        "Product",
        "Varied example datasets",
        PASS if valid else WARN,
        f"{len(examples):,} example CSV files are available.",
        "Add at least three varied business examples." if not valid else "",
    )


def _test_structure_check(root: Path) -> ReadinessCheck:
    test_files = list((root / "tests").glob("test_*.py"))
    valid = len(test_files) >= 10
    return _check(
        "TEST-001",
        "Engineering",
        "Automated test coverage structure",
        PASS if valid else FAIL,
        f"{len(test_files):,} automated test modules are present.",
        "Add automated tests for every launch-critical module." if not valid else "",
    )


def _ci_checks(root: Path) -> tuple[ReadinessCheck, ...]:
    workflow = _read(root / ".github/workflows/ci.yml")
    install = _actual_run_step(
        workflow,
        r"(?:python\s+-m\s+pip|pip)\s+install",
    )
    tests = _actual_run_step(
        workflow,
        r"(?:python\s+-m\s+pytest|pytest)(?:\s|$)",
    )
    lint = _actual_run_step(
        workflow,
        r"(?:ruff|flake8|pylint|mypy)(?:\s|$)",
    )
    return (
        _check(
            "CI-001",
            "Engineering",
            "CI installs dependencies",
            PASS if install else FAIL,
            (
                "CI contains a real dependency-install step."
                if install
                else "CI does not install project dependencies."
            ),
            (
                "Replace placeholder commands with pip install "
                "-r requirements.txt."
                if not install
                else ""
            ),
        ),
        _check(
            "CI-002",
            "Engineering",
            "CI runs the test suite",
            PASS if tests else FAIL,
            (
                "CI contains a real pytest step."
                if tests
                else "CI does not execute pytest."
            ),
            (
                "Add python -m pytest -q to the CI workflow."
                if not tests
                else ""
            ),
        ),
        _check(
            "CI-003",
            "Engineering",
            "CI runs a static-quality check",
            PASS if lint else WARN,
            (
                "CI contains a static-quality command."
                if lint
                else "No real lint, format or type-check command was found."
            ),
            (
                "Add a focused Ruff or equivalent check."
                if not lint
                else ""
            ),
        ),
    )


def _dependency_check(root: Path) -> ReadinessCheck:
    requirements = _read(root / "requirements.txt")
    valid, unbounded = _bounded_requirements(requirements)
    return _check(
        "DEP-001",
        "Engineering",
        "Dependencies are intentionally bounded",
        PASS if requirements and valid else FAIL,
        (
            "Every runtime and test dependency has a lower and upper bound."
            if requirements and valid
            else "Unbounded or missing entries: " + ", ".join(unbounded)
        ),
        "Add intentional compatible version ranges." if not valid else "",
    )


def _python_support_check(root: Path) -> ReadinessCheck:
    readme = _read(root / "README.md")
    workflow = _read(root / ".github/workflows/ci.yml")
    documented = "Python 3.11+" in readme
    ci_version = re.search(
        r"python-version:\s*['\"]?3\.11",
        workflow,
    )
    valid = documented and ci_version is not None
    return _check(
        "DEP-002",
        "Engineering",
        "Supported Python version is defined",
        PASS if valid else FAIL,
        (
            "README and CI identify Python 3.11."
            if valid
            else "Python support is not aligned between README and CI."
        ),
        "Document and test the same supported Python version." if not valid else "",
    )


def _tracked_artifact_check(
    tracked: tuple[Path, ...],
) -> ReadinessCheck:
    pattern = re.compile(
        r"(^|/)(?:__pycache__|\.pytest_cache|\.idea|\.venv)(/|$)"
        r"|\.pyc$"
    )
    findings = [
        str(path)
        for path in tracked
        if pattern.search(path.as_posix())
    ]
    return _check(
        "REPO-001",
        "Repository hygiene",
        "Generated artifacts are not tracked",
        FAIL if findings else PASS,
        (
            "Tracked generated files: " + ", ".join(findings)
            if findings
            else "No cache, IDE, virtualenv or bytecode files are tracked."
        ),
        (
            "Remove generated files from Git and expand .gitignore."
            if findings
            else ""
        ),
    )


def _secret_check(
    root: Path,
    tracked: tuple[Path, ...],
) -> ReadinessCheck:
    findings = _secret_findings(root, tracked)
    return _check(
        "SEC-001",
        "Privacy and security",
        "No obvious tracked secrets",
        FAIL if findings else PASS,
        (
            "Potential secret material: " + ", ".join(findings)
            if findings
            else "No sensitive filenames or credential-like assignments "
            "were detected in tracked files."
        ),
        "Remove and rotate every exposed credential." if findings else "",
    )


def _security_policy_check(root: Path) -> ReadinessCheck:
    policy = _read(root / ".github/SECURITY.md")
    has_contact = bool(
        re.search(
            r"(?:@|mailto:|security\s+advisory|contact)",
            policy,
            flags=re.IGNORECASE,
        )
    )
    detailed = len(policy.split()) >= 60
    valid = has_contact and detailed
    return _check(
        "SEC-002",
        "Privacy and security",
        "Actionable security-reporting policy",
        PASS if valid else FAIL,
        (
            "The policy includes a private reporting path and useful detail."
            if valid
            else "The security policy lacks an actionable private reporting "
            "path or sufficient handling guidance."
        ),
        "Document supported versions, private contact and response process." if not valid else "",
    )


def _privacy_contract_check(
    review: SecurityReview,
) -> ReadinessCheck:
    relevant = tuple(
        check
        for check in review.checks
        if check.check_id.startswith("PRIV-")
    )
    failed = [
        check.check_id
        for check in relevant
        if check.status == FAIL
    ]
    valid = bool(relevant) and not failed
    return _check(
        "SEC-003",
        "Privacy and security",
        "Local-first privacy controls",
        PASS if valid else FAIL,
        (
            "Upload handling, runtime clients, error details and privacy "
            "documentation match the local-first contract."
            if valid
            else "Failed privacy controls: " + ", ".join(failed)
        ),
        "Run python scripts/security_review.py --root . and resolve failures."
        if not valid
        else "",
    )


def _dependency_security_check(
    review: SecurityReview,
) -> ReadinessCheck:
    dependency = next(
        (
            check
            for check in review.checks
            if check.check_id == "DEP-SEC-001"
        ),
        None,
    )
    valid = dependency is not None and dependency.status == PASS
    return _check(
        "DEP-003",
        "Engineering",
        "Dependency vulnerability gate",
        PASS if valid else FAIL,
        (
            "A bounded pip-audit dependency and strict CI scan are configured."
            if valid
            else "The repository lacks a complete dependency vulnerability "
            "gate."
        ),
        "Add requirements-security.txt and run pip-audit strictly in CI."
        if not valid
        else "",
    )


def _readme_scope_check(root: Path) -> ReadinessCheck:
    readme = _read(root / "README.md")
    required_terms = (
        "Analysis Assistant",
        "Export & Share",
        "Data Quality",
    )
    missing = [
        term for term in required_terms if term not in readme
    ]
    return _check(
        "DOC-002",
        "Documentation",
        "README matches shipped navigation",
        FAIL if missing else PASS,
        (
            "Missing shipped capabilities: " + ", ".join(missing)
            if missing
            else "README includes the current core application pages."
        ),
        "Update README features, workflow and screenshots." if missing else "",
    )


def _changelog_check(root: Path) -> ReadinessCheck:
    changelog = _read(root / "CHANGELOG.md")
    missing = [
        version
        for version in ("0.3", "0.4", "0.5", "0.6")
        if f"[{version}" not in changelog
    ]
    return _check(
        "REL-001",
        "Release",
        "Changelog covers delivered milestones",
        FAIL if missing else PASS,
        (
            "Missing milestone sections: " + ", ".join(missing)
            if missing
            else "Changelog includes the delivered 0.3–0.6 milestones."
        ),
        "Add accurate dated or unreleased sections for delivered work." if missing else "",
    )


def _release_status_check(root: Path) -> ReadinessCheck:
    notes = _read(root / "releases/v1.0/release_notes.md")
    candidate = bool(
        re.search(
            r"Status:\s*(?:Release candidate|Released)",
            notes,
            flags=re.IGNORECASE,
        )
    )
    return _check(
        "REL-002",
        "Release",
        "v1.0 has an explicit release-candidate status",
        PASS if candidate else FAIL,
        (
            "v1.0 is marked as a release candidate or released."
            if candidate
            else "v1.0 is still marked as planned."
        ),
        "Freeze scope, resolve blockers and mark the release candidate." if not candidate else "",
    )


def _release_asset_check(root: Path) -> ReadinessCheck:
    demo = root / "releases/v1.0/demo.gif"
    try:
        header = demo.read_bytes()[:6]
    except OSError:
        header = b""
    valid = header in {b"GIF87a", b"GIF89a"}
    return _check(
        "REL-003",
        "Release",
        "v1.0 demo asset is a valid GIF",
        PASS if valid else FAIL,
        (
            "The launch demo has a valid GIF signature."
            if valid
            else "releases/v1.0/demo.gif is missing or still a placeholder."
        ),
        "Record and add the verified final-product demo." if not valid else "",
    )


def _version_metadata_check(root: Path) -> ReadinessCheck:
    version_file = root / "app_core/version.py"
    text = _read(version_file)
    valid = bool(
        re.search(
            r"(?:__version__|PRODUCT_VERSION)\s*=\s*['\"]1\.0",
            text,
        )
    )
    return _check(
        "REL-004",
        "Release",
        "Single product-version source",
        PASS if valid else FAIL,
        (
            "A v1.0 product-version source is present."
            if valid
            else "No canonical v1.0 version module was found."
        ),
        "Add app_core/version.py and reuse it in export metadata." if not valid else "",
    )


def _release_process_check(root: Path) -> ReadinessCheck:
    process = _read(root / "docs/10_RELEASE_PROCESS.md")
    required_terms = (
        "clean install",
        "pytest",
        "release candidate",
        "tag",
        "rollback",
    )
    missing = [
        term for term in required_terms
        if term not in process.lower()
    ]
    return _check(
        "REL-005",
        "Release",
        "Repeatable release process",
        FAIL if missing else PASS,
        (
            "Missing process topics: " + ", ".join(missing)
            if missing
            else "Release documentation covers validation, publication and "
            "rollback."
        ),
        "Expand the release process into an executable checklist." if missing else "",
    )


def audit_repository(
    root: Path,
) -> ReleaseReadinessReport:
    """Run deterministic static launch-readiness checks."""

    root = root.resolve()
    tracked = _tracked_files(root)
    security_review = audit_security(root)
    checks = [
        _required_documentation_check(root),
        _application_structure_check(root),
        _sample_data_check(root),
        _example_coverage_check(root),
        _test_structure_check(root),
        *_ci_checks(root),
        _dependency_check(root),
        _python_support_check(root),
        _dependency_security_check(security_review),
        _tracked_artifact_check(tracked),
        _secret_check(root, tracked),
        _security_policy_check(root),
        _privacy_contract_check(security_review),
        _readme_scope_check(root),
        _changelog_check(root),
        _release_status_check(root),
        _release_asset_check(root),
        _version_metadata_check(root),
        _release_process_check(root),
    ]
    return ReleaseReadinessReport(checks=tuple(checks))


def report_to_markdown(
    report: ReleaseReadinessReport,
) -> str:
    """Render a portable readiness report."""

    lines = [
        "# v1.0 Release Readiness Audit",
        "",
        f"**Overall status:** {report.overall_status}",
        "",
        (
            f"**Summary:** {report.pass_count} PASS · "
            f"{report.warning_count} WARN · {report.fail_count} FAIL"
        ),
        "",
        "| ID | Category | Check | Status | Detail |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        detail = check.detail.replace("|", "\\|")
        lines.append(
            f"| {check.check_id} | {check.category} | {check.title} | "
            f"**{check.status}** | {detail} |"
        )

    failed = [
        check
        for check in report.checks
        if check.status in {FAIL, WARN}
    ]
    lines.extend(["", "## Required follow-up", ""])
    if failed:
        for check in failed:
            lines.append(
                f"- **{check.check_id} · {check.status}:** "
                f"{check.remediation}"
            )
    else:
        lines.append("- No static blockers detected.")

    lines.extend(
        [
            "",
            "## Scope note",
            "",
            (
                "This checker validates repository evidence. It does not "
                "replace manual UX, accessibility, performance, clean-install "
                "or security review."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit Universal CSV Dashboard release readiness.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 when a FAIL is present.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    report = audit_repository(args.root)
    print(report_to_markdown(report))
    return 1 if args.strict and report.fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
