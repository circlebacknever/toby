---
name: toby-swd-twelve-factor
description: >-
  Contains Toby's twelve-factor checks for new processes, config, secrets, and
  backing services. Use it for a new process, worker, scheduled job, config
  value, secret, or backing service. Skip it for a change that adds none of
  these.
---

# Toby SWD Twelve-Factor

Check the diff against each factor below that it touches.

## Dependencies

Declare every imported package in the manifest and lockfile, and invoke a system binary (such as `ffmpeg`) only when the Dockerfile or buildpack installs it.

## Config

Read every deploy-varying value from environment variables, validate required variables at startup, and redact secrets from validation errors and serialized config objects. When the repo has a config module (`references/config.md`), read all env vars through it and check the diff for raw `os.environ`, `process.env`, or `import.meta.env` reads outside it. Never branch on environment names (`NODE_ENV === "production"`) in domain code, and never put secrets in client-bundled `VITE_*`, `NEXT_PUBLIC_*`, or `EXPO_PUBLIC_*` variables.

## Backing services

Connect to every database, cache, queue, and third-party API through a URL and credentials from config, and check the diff for hardcoded hosts (`localhost:5432`).

## Build, release, run

Run database migrations in the deploy release step, and don't run them during web worker startup (single-host Kamal setups are the one exception). Check startup code for `migrate`, `db.create_all()`, or `sequelize.sync()`.

## Processes

Store any state that a later request reads in a backing service (database, Redis, object storage). Never keep cross-request state in module-level variables, in-memory sessions, or container-local disk without a persistent volume. Pure computation caches (`lru_cache`) with bounded size may stay in memory.

## Port binding

Read the listening port from config (`PORT`), and check `listen()` or `run()` calls for hardcoded ports.

## Concurrency

Run new consumers and scheduled tasks in the repo's worker process or platform scheduler. Never start them inside web startup hooks that every process, console, and migration runs (`config/initializers/` in Rails, `AppConfig.ready()` in Django, or multi-worker FastAPI lifespan hooks). Check startup code for `setInterval`, `node-cron`, `APScheduler`, `rufus-scheduler`, or background threads.

## Disposability

Where the repo has health checks or runs behind a load balancer, handle `SIGTERM` and readiness checks as `references/shutdown.md` describes.

## Dev/prod parity

Use the same database, queue, and cache engines in development and tests as in production.

## Logs

Write service logs to `stdout` and CLI logs to `stderr` (keeping `stdout` for program output), without `FileHandler` or local `.log` files.

## Admin processes

Write backfills that new code requires at deploy time as migrations. Put slow or one-off maintenance tasks in repo management commands that reuse the app's config and models.
