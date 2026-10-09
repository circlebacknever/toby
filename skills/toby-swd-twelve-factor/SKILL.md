---
name: toby-swd-twelve-factor
description: >-
  Contains Toby's twelve-factor checks for new processes, config, secrets, and
  backing services. Entry skills open this file by path. Do not trigger it from
  a user request alone.
disable-model-invocation: true
---

# Toby SWD Twelve-Factor

Check the diff against each factor below that it touches.

## Dependencies

Declare every package in the manifest and the lockfile. Call a system tool, such as `ffmpeg`, only when the Dockerfile or buildpack installs it. Check that each new import has a manifest entry, and each subprocess call names a tool the image installs.

## Config

Read each value that changes between deploys from the environment, and fail at startup when a required value is missing or malformed. When the repo has a config module, read the value through it, and search the diff for `os.environ`, `process.env`, and `import.meta.env` outside it. Otherwise read it at startup, with the same call the repo uses for its other values. Write a config module only in a new service or when the user asks, as `references/config.md` describes. Do not branch on the environment's name, such as `NODE_ENV === "production"`, in application code. Every `VITE_*`, `NEXT_PUBLIC_*`, and `EXPO_PUBLIC_*` value is compiled into the client bundle, so put no secret there.

## Backing services

Attach each database, cache, queue, and third-party API through a URL and credentials from config. Search the diff for a hard-coded host, such as `localhost:5432`.

## Build, release, run

Run migrations as a release step, such as a release command in the deploy config or a step in the deploy script. An app that starts one new instance per deploy, such as Rails' default Kamal setup on one host, may migrate at startup. Search startup code for `migrate`, `db.create_all()`, or `sequelize.sync()`.

## Processes

Keep data that a later request reads in a backing service, such as the database, Redis, or object storage. This rule covers a module-level dict, an in-memory session, and a file on the local disk of a container without a volume. A cache that only saves work, such as `lru_cache` on a pure function, can stay in the process. Look for module-level state that one request writes and a later request reads.

## Port binding

Read the port the app listens on from config, such as `PORT`. Search the diff for a hard-coded port in `listen()` or `run()`.

## Concurrency

Run a new consumer or scheduled task in the repo's existing worker, such as a Celery worker, when it has one. Otherwise run it as its own process type, such as a `worker:` line in the Procfile, or as the platform's scheduled job. A single-host app may run them inside the web server, such as through Solid Queue's Puma plugin.

Never start a consumer, scheduler, or timer loop from startup code that every process runs, such as a Rails initializer or Django's `AppConfig.ready()`. Consoles, migrations, and other workers run that code too. A FastAPI lifespan task runs once per web worker, so start these loops there only when the deploy config allows one worker and one instance. Search the diff's startup code, such as `config/initializers/` in Rails, a FastAPI lifespan task, or `AppConfig.ready()`. Look for `setInterval`, `node-cron`, `APScheduler`, `rufus-scheduler`, a consumer loop, or a thread.

## Disposability

Add a shutdown hook or health check only where the repo has one, or in a new web service behind a load balancer. Open `references/shutdown.md` for the steps on `SIGTERM` and the health checks.

## Dev/prod parity

Use the same kind of database, queue, and cache in development and tests as in production. Compare the database engine in the test settings with the production one.

## Logs

Write a service's logs to stdout, and let the platform collect them. Write a CLI's logs to stderr, because stdout holds the program's output. Search the diff for `FileHandler`, a rotating file handler, or a `.log` path.

## Admin processes

Write a backfill that new code depends on as a data migration beside the schema change. A slow backfill or a one-off fix goes in a command in the repo, such as a Django management command. Look for a script that builds its own database connection from a hard-coded URL.
