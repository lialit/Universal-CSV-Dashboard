# Support

Universal CSV Dashboard is an open-source project maintained on a best-effort basis. This guide explains where to ask for help and what information makes a request actionable.

## Choose the correct route

### Something is broken

Open a structured **Bug report** in GitHub Issues.

Include:

- the affected version or commit;
- your operating system and Python version;
- expected and actual behaviour;
- complete reproduction steps;
- the full error message;
- a minimal synthetic CSV when the problem depends on data shape.

Do not attach confidential exports, credentials, personal data, or client files.

### You want a product change

Open a structured **Feature request**. Explain the user problem, the desired outcome, and why existing behaviour does not solve it. A proposed implementation is welcome but not required.

### You need installation or usage help

Review these documents first:

- [`START_HERE.md`](START_HERE.md) for installation and first use;
- [`docs/README.md`](docs/README.md) for detailed documentation;
- [`docs/ISSUE_AND_PR_GUIDE.md`](docs/ISSUE_AND_PR_GUIDE.md) for issue routing and evidence requirements.

If the documentation does not resolve the problem, use the repository issue chooser and select the usage or documentation route. Keep the example non-sensitive.

### You found a security problem

Do **not** post vulnerability details in a public issue. Follow [`.github/SECURITY.md`](.github/SECURITY.md) and use GitHub's private security advisory form.

## Support boundaries

Maintainers can help with reproducible behaviour in the published application and repository. The project does not promise:

- guaranteed response or resolution times;
- private consulting through public issues;
- analysis of confidential business datasets;
- custom dashboard development as part of open-source support;
- recovery of damaged source files;
- validation that a business conclusion is correct for a specific organisation;
- support for unmaintained forks or modified deployments.

Questions about professional customisation should remain separate from public bug triage and must not include private client data.

## Response expectations

Requests are reviewed as maintainer capacity allows. Clear reproduction evidence and a focused scope make a response more likely. Duplicate, incomplete, unsafe, or out-of-scope requests may be closed with a link to the appropriate documentation.

A lack of immediate response does not indicate acceptance of a bug, feature, security severity, or delivery commitment.

## Before posting

1. Confirm the problem still occurs on the latest stable release or current `main`.
2. Search existing issues for the same behaviour.
3. Reduce the example to the smallest synthetic case.
4. Remove secrets and identifying information.
5. Select the correct public or private reporting route.
