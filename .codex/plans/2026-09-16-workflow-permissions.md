# Explicit CI token permissions

Owner: Learning Resources security repair PR. The existing CI workflow omitted permissions, leaving token scope dependent on repository defaults. Grant contents: read explicitly; all other scopes default to none. Checkout and Python test/lint installation need no write permissions. Preserve all existing test and lint steps and pinned actions. Bound the job to ten minutes.

Verification: actionlint validates the changed workflow. This is a source-level repair for the observed missing-workflow-permissions finding; hosted execution and security alert clearance require separate evidence. Existing zero-step hosted failures are not repaired or explained by this permission declaration.
