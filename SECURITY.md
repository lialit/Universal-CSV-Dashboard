# Security Policy

## Supported versions

Security fixes are provided for the latest stable release and the current `main`
branch when the issue affects unreleased code.

| Version | Supported |
| --- | --- |
| Latest stable release | Yes |
| Current `main` branch | Yes |
| Older releases | Best effort |

## Reporting a vulnerability

Please do not open a public Issue for a suspected vulnerability.

Use the repository's private **Security** tab and select **Report a
vulnerability** to open a private security advisory. Include:

- the affected version or commit;
- a clear description of the issue and potential impact;
- minimal reproduction steps or a proof of concept;
- relevant operating system, Python and browser details;
- suggested remediation, if known.

Do not attach real customer datasets, credentials, tokens, private exports or
other confidential material. Use synthetic data and redact secrets from logs and
screenshots.

## What to expect

The maintainer will:

1. acknowledge the report when it is reviewed;
2. assess severity, scope and reproducibility;
3. coordinate a fix and release where appropriate;
4. credit the reporter if requested and safe to do so.

Response and remediation time depend on severity and maintainer availability. No
specific service-level agreement is guaranteed.

## Scope

Examples of security-relevant reports include:

- arbitrary code execution or unsafe file handling;
- path traversal or unintended filesystem access;
- leakage of uploaded CSV data, session state or generated exports;
- secrets committed to the repository or exposed by the application;
- dependency vulnerabilities with a practical impact on this project;
- unsafe HTML, formula injection or export behavior;
- authentication or deployment misconfiguration in an official hosted demo.

General bugs, performance issues and feature requests should use the public Issue
templates instead.

## Safe testing

Test only against systems and data you own or are authorized to use. Avoid
privacy violations, destructive actions, service disruption and accessing other
users' data.

## Disclosure

Please allow reasonable time for validation and remediation before public
disclosure. Public details may be coordinated through a GitHub Security Advisory
and release notes after a fix is available.
