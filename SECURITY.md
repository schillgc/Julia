# Security and local configuration

This repository contains multiple independent learning and application projects. Treat every Django application and each external integration as a separate deployment boundary.

## Credential handling

- Never commit real environment files, Python credential/secret modules, OAuth client JSON, OAuth token caches, API keys, passwords, or signing keys.
- `.gitignore` excludes common Python credential-module and private-key filenames for future files. Ignore rules do not remove files that are already tracked. The tracked Oxford Dictionary `credentials.py` compatibility module reads only `OXFORD_DICTIONARIES_APP_ID` and `OXFORD_DICTIONARIES_APP_KEY` from the process environment; it contains no committed API credentials. Keep real values in a local secret manager or environment, never in source control.
- Copy `.env.example` to a local `.env` file or export only the variables required by the project being run. The repository ignores real environment files.
- Each Django application requires its own `<PROJECT>_DJANGO_SECRET_KEY`, debug flag, and host allowlist. Generate a unique random signing key per deployment, at least 50 characters long with at least 5 distinct characters. Use `python -c 'import secrets; print(secrets.token_urlsafe(64))'`. Development uses `<PROJECT>_DJANGO_DEBUG=true` and loopback-only hosts; production must set `DEBUG=false` and an explicit comma-separated host allowlist.
- Google Calendar OAuth client JSON and user token JSON belong outside Git. The old committed pickle token is removed; re-authorize after rotating the OAuth client.
- Keep YouTube OAuth client material and token caches local and ignored.
- Set Oxford Dictionaries, Mailchimp, and OpenAI credentials in the environment. The Oxford Dictionary examples no longer import the tracked legacy credential module; they fail closed when the two required Oxford environment variables are absent. The tracked module still requires private owner review and rotation of any values found inside.
- Budget and job-analysis amounts are read from local environment variables. Do not put personal financial, compensation, or family information in tracked source files.

## Exposure response

Some credentials and private values were present in older commits of this public repository. Removing them from the current branch does not erase Git history, forks, caches, or existing clones. Treat every previously committed credential as compromised:

1. Revoke and replace the Google OAuth client secret and invalidate existing Google Calendar refresh tokens.
2. Rotate the Oxford Dictionaries app key, Mailchimp Transactional/Marketing keys, Google Maps API keys, and any OpenAI key that may have been present in local configuration.
3. Generate new unique Django signing keys for every affected deployment; invalidate sessions signed with old keys.
4. Restrict replacement provider keys by API, referrer, origin, quota, and environment wherever supported.
5. Review provider usage and billing logs for unexpected activity.

This repository's visibility cannot be changed through the connected GitHub operations available in this workspace. Because historical secrets and private data were committed, switch the repository to **private** in GitHub repository Settings before further public distribution. This commit does not rewrite history or remove existing copies.

## Verification scope

The security workflow checks the current source tree for the exposed credential patterns and validates the environment-based settings contracts. It does not certify every legacy application, its dependencies, third-party service configuration, data model, or production deployment. Validate each application independently before deploying it.
