# Test dependencies

This file has the rules for a test that depends on a database engine, a third-party provider, another process, or a library version.

## Database engine

Django drops `select_for_update` on SQLite, so a test there cannot show that a lock works.

## Third-party providers

Mock the function in the one module that calls the provider, as "Default structure" in `toby-swd-architecture` describes. To test that module, stub the HTTP call at the network edge with a tool such as `responses`, `nock`, or WebMock.

## Boundaries

Across a process, sandbox, or hardware boundary, fake the channel or simulate the environment, and test each side against the contract.

## Versions and machines

When a result depends on a library or platform version, record the version. When the system must give the same output across runs or machines, test that determinism as part of the contract.
