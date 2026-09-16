# Explicit CI token permissions

Owner: Learning Resources security repair PR. The existing CI workflow omitted permissions, leaving token scope dependent on repository defaults. Grant contents: read explicitly; all other scopes default to none. Checkout and Python test/lint installation need no write permissions. Preserve all existing test and lint steps and pinned actions. Bound the job to ten minutes.

Verification: actionlint validates the changed workflow. This is a source-level repair for the observed missing-workflow-permissions finding; hosted execution and security alert clearance require separate evidence. Existing zero-step hosted failures are not repaired or explained by this permission declaration.

## Executed relay follow-up

Relay run https://github.com/4444J99/organvm-ci-relay/actions/runs/35111583330 executed main b5f3aba021238135a12497a121f78b3ec2985eb0: 14 tests passed, Ruff rejected timezone.utc (UP017). Use the equivalent datetime.UTC alias supported by the declared Python >=3.11 floor. Preserve lint coverage and the earlier workflow permission/timeout repair. Verify tests and the strict relay Ruff selection, then submit this changed head once through the integration rail.
