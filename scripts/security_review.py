from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


PASS = "PASS"
FAIL = "FAIL"

NETWORK_CLIENTS = (
    "aiohttp",
    "anthropic",
    "google.genai",
    "httpx",
    "openai",
    "requests",
    "socket",
    "urllib.request",
)


@dataclass(frozen=True)
class SecurityCheck:
    """One deterministic security or privacy control."""

    check_id: str
    title: str
    status: str
    detail: str


@dataclass(frozen=True)
class SecurityReview:
    """Static review of the repository's local-first security controls."""

    checks: tuple[SecurityCheck, ...]

    @property
    def failed(self) -> tuple[SecurityCheck, ...]:
        return tuple(
            check for check in self.checks if check.status == FAIL
        )

    @property
    def passed(self) -> bool:
        return not self.failed


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _check(
    check_id: str,
    title: str,
    valid: bool,
    passed_detail: str,
    failed_detail: str,
) -> SecurityCheck:
    return SecurityCheck(
        check_id=check_id,
        title=title,
        status=PASS if valid else FAIL,
        detail=passed_detail if valid else failed_detail,
    )


def _runtime_python_files(root: Path) -> tuple[Path, ...]:
    candidates = [root / "app.py"]
    for directory in ("app_core", "views"):
        path = root / directory
        if path.is_dir():
            candidates.extend(path.rglob("*.py"))
    return tuple(path for path in candidates if path.is_file())


def _network_client_findings(root: Path) -> list[str]:
    clients = "|".join(re.escape(client) for client in NETWORK_CLIENTS)
    import_pattern = re.compile(
        rf"^\s*(?:from|import)\s+({clients})(?:\.|\s|$)",
        flags=re.MULTILINE,
    )
    findings: list[str] = []

    for path in _runtime_python_files(root):
        match = import_pattern.search(_read(path))
        if match:
            findings.append(
                f"{path.relative_to(root)} imports {match.group(1)}"
            )

    requirements = _read(root / "requirements.txt").lower()
    direct_packages = {
        re.split(r"[<>=!~\[]", line.strip(), maxsplit=1)[0]
        for line in requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    for client in NETWORK_CLIENTS:
        package = client.split(".", maxsplit=1)[0]
        if package in direct_packages:
            findings.append(
                f"requirements.txt directly includes {package}"
            )

    return findings


def audit_security(root: Path) -> SecurityReview:
    """Review repository evidence for the local-first security contract."""

    root = root.resolve()
    upload = _read(root / "views/upload.py")
    data = _read(root / "app_core/data.py")
    runtime = "\n".join(
        _read(path) for path in _runtime_python_files(root)
    )
    config = _read(root / ".streamlit/config.toml")
    privacy = _read(root / "docs/12_SECURITY_PRIVACY.md")
    security_requirements = _read(
        root / "requirements-security.txt"
    )
    workflow = _read(root / ".github/workflows/ci.yml")

    in_memory = (
        "uploaded_file.getvalue()" in upload
        and "BytesIO(file_bytes)" in data
        and "NamedTemporaryFile" not in runtime
        and "TemporaryDirectory" not in runtime
    )
    network_findings = _network_client_findings(root)
    hidden_errors = bool(
        re.search(
            r"showErrorDetails\s*=\s*['\"]none['\"]",
            config,
        )
    )
    privacy_terms = (
        "local-first",
        "temporary",
        "session state",
        "external processing",
        "excel",
        "security",
    )
    privacy_complete = (
        len(privacy.split()) >= 300
        and all(term in privacy.lower() for term in privacy_terms)
    )
    dependency_gate = (
        "pip-audit" in security_requirements
        and ">=" in security_requirements
        and "<" in security_requirements
        and bool(
            re.search(
                r"python\s+-m\s+pip_audit\s+-r\s+"
                r"requirements\.txt\s+--strict",
                workflow,
            )
        )
    )

    checks = (
        _check(
            "PRIV-001",
            "Uploaded CSV remains in the session data path",
            in_memory,
            "Uploads are parsed from bytes without an application-managed "
            "row-level temporary file.",
            "The upload path does not provide complete in-memory evidence.",
        ),
        _check(
            "PRIV-002",
            "No external runtime client is configured",
            not network_findings,
            "No direct external network or AI client was found in runtime "
            "imports or direct requirements.",
            "Potential external clients: " + ", ".join(network_findings),
        ),
        _check(
            "PRIV-003",
            "Detailed client errors are hidden",
            hidden_errors,
            "Streamlit client error details are disabled.",
            "Set [client].showErrorDetails to \"none\".",
        ),
        _check(
            "PRIV-004",
            "Security and privacy behavior is documented",
            privacy_complete,
            "The privacy document covers data flow, temporary handling, "
            "exports, external processing and security limitations.",
            "The privacy document is missing or incomplete.",
        ),
        _check(
            "DEP-SEC-001",
            "Known dependency vulnerabilities are audited in CI",
            dependency_gate,
            "A bounded pip-audit tool and strict CI scan are configured.",
            "Add a bounded pip-audit dependency and strict CI command.",
        ),
    )
    return SecurityReview(checks=checks)


def review_to_markdown(review: SecurityReview) -> str:
    status = "PASS" if review.passed else "FAIL"
    lines = [
        "# Security and Privacy Review",
        "",
        f"**Overall status:** {status}",
        "",
        "| ID | Control | Status | Detail |",
        "|---|---|---|---|",
    ]
    for check in review.checks:
        detail = check.detail.replace("|", "\\|")
        lines.append(
            f"| {check.check_id} | {check.title} | "
            f"**{check.status}** | {detail} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify local-first security and privacy controls.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current directory.",
    )
    args = parser.parse_args()

    review = audit_security(args.root)
    print(review_to_markdown(review), end="")
    return 0 if review.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
