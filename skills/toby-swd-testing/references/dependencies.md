# Test dependencies

This file covers tests that depend on a database engine, a third-party provider, another process, or a library version.

## Database engine

Run locking and concurrency tests against the production database engine, because SQLite ignores `SELECT ... FOR UPDATE`.

## Third-party providers

In tests for callers, mock the function on your provider module (`toby-swd-architecture`). In tests for the provider module itself, stub the outbound HTTP call with a library such as `responses`, `nock`, or WebMock.

## Boundaries

Across a process, sandbox, or hardware boundary, fake the transport channel and test each side against the shared message contract.

## Versions and machines

When a result depends on a library or platform version, record the version. When the system must return identical output across runs or machines, assert that determinism in a test.
