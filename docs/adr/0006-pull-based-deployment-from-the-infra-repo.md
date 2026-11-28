# 0006: Pull-based deployment from the infra repo

Date: 2026-11-28
Status: accepted

## Context

Four repos produce things that run in production. The host is a small machine that cannot be reached from outside, and all repos are public. A deployment must not need secrets in plain text on GitHub, and it must be visible on GitHub whether it worked.

A self-hosted GitHub Actions runner on the host would let workflows start deployments. GitHub advises against self-hosted runners for public repos, because pull requests from forks can run code on the host, and a runner costs memory the host does not have.

## Decision

- **The infra repo decides what runs.** The Compose stack, the image versions (`compose/prod/versions.env`) and the encrypted secrets live in `wortlaut-infra`. `main` of that repo needs a pull request with a green CI check. Only the deploy workflows commit directly, through a deploy key.
- **Each application repo has a manual workflow Deploy to PROD.** It runs the CI, builds a `linux/arm64` image on an Arm runner, publishes it to ghcr.io as `sha-<commit>` and commits the tag to the infra repo. The deploy key is a secret of a protected environment that only `main` can use. The packages are public, so the host needs no registry login.
- **The host pulls.** A timer runs `compose/prod/deploy.sh` every few minutes. The script does nothing when the revision is already deployed. Otherwise it decrypts the secrets into memory, pulls the images, starts what changed, waits until every service is healthy and removes images that are not part of the stack.
- **Secrets are encrypted with SOPS and age.** The repo holds only ciphertext, with one age key per person or machine that has to read it. Secrets reach the containers as environment variables. Nothing sensitive is in a workflow, an image or a plain file.
- **The result is reported back.** After a deployment the host pushes an info commit to the branch `prod-status`. A workflow on that branch sets the commit status `deploy/prod` on the deployed commit and fails when the deployment failed, which also triggers the notification mails. Deploy to PROD waits for the result of its commit and fails with it.

## Consequences

- No inbound access to the host, no GitHub credentials on it except a key that can only write the info commits, and no code from pull requests ever runs there.
- A release takes up to the timer interval longer than a push-based one, and the log of a deployment lives on the host. The result on GitHub covers the common case.
- Changing a secret is a pull request in the infra repo. It rolls out like any other revision.
- A lost age key can no longer decrypt the secrets. Keys have to be kept safe, and the secrets can be re-encrypted for a new key from any machine that holds a current one.
- The deploy keys of the infra repo can bypass the branch rule. They are narrow in scope and stored as protected secrets, but they are the most powerful credential of the setup.
- Rolling back means running Deploy to PROD from an older commit or changing the tag through a pull request.
