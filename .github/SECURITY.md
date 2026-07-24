# Security Policy

## Supported versions

Universal CSV Dashboard is preparing its first stable release.

| Version | Security support |
|---|---|
| `1.0.0-rc.x` and `main` | Supported |
| Earlier development snapshots | Not supported |

Security fixes are applied to the current release-candidate line. Support for
additional stable versions will be documented when those versions exist.

## Report a vulnerability privately

Do not open a public issue for a suspected vulnerability.

Use GitHub's private security advisory form:

<https://github.com/lialit/Universal-CSV-Dashboard/security/advisories/new>

If the private form is unavailable, open a public issue containing only a
request for private contact. Do not include exploit details, credentials,
personal information or client data in that issue.

Please include:

- the affected version or commit;
- the affected component;
- clear reproduction steps using synthetic data;
- the potential impact;
- any suggested mitigation;
- whether the issue is already public.

Never attach a real confidential CSV. Build the smallest synthetic example
that demonstrates the issue.

## What to expect

Maintainers aim to:

1. acknowledge a complete report within five business days;
2. validate severity and affected versions;
3. coordinate a fix and a safe disclosure timeline;
4. provide status updates when practical;
5. publish affected versions and upgrade guidance with the fix.

Response times are targets, not a guarantee. Complex reports may require more
time. Please avoid public disclosure until users have had a reasonable
opportunity to update.

## Security scope

Reports are especially useful when they concern:

- unsafe CSV parsing or formula injection;
- exposure of uploaded or exported business data;
- unintended network transmission;
- secrets committed to the repository;
- vulnerable direct or transitive dependencies;
- unsafe project/configuration deserialization;
- path traversal or arbitrary file access;
- sensitive information in logs or error messages.

Reports about analytical correctness are also important, but ordinary
calculation defects should use the bug-report template unless they expose or
corrupt confidential data.

## Product security model

The default product is local-first:

- uploaded CSV bytes are processed in the active Streamlit session;
- the application does not send CSV values to an external AI service;
- saved project files contain configuration and schema metadata, not raw rows;
- PDF and Excel exports are created locally;
- row-level Excel exports must be treated as sensitive copies of the source.

This model does not protect data after a user downloads, copies or shares an
export. A hosted Streamlit deployment also introduces the operator and hosting
environment into the trust boundary.

See [`docs/12_SECURITY_PRIVACY.md`](../docs/12_SECURITY_PRIVACY.md) for the
complete data-flow and privacy review.

## Responsible disclosure

Good-faith research that avoids privacy violations, service disruption and
destructive testing is welcome. Do not access data that is not yours, and stop
testing if confidential information becomes visible.
