# End-to-end harnesses

This file lists the files, folders, and markers that identify an end-to-end test harness in each stack.

- JavaScript and TypeScript repos use `playwright.config`, `cypress.config`, or `supertest` in a test file.
- Python repos use a `tests/e2e` folder, a pytest marker such as `e2e` or `integration`, or Django's `self.client`, DRF's `APIClient`, or pytest-django's `client` fixture.
- Go repos use `httptest.NewServer` or a `//go:build e2e` build tag.
- Ruby repos use Rails request specs in `spec/requests`, integration tests in `test/integration`, or system tests in `test/system` or `spec/system`.
- Mobile repos use `.detoxrc`, a `.maestro` folder, XCUITest, or Espresso.
- Multi-service repos use `docker-compose.test.yml`, testcontainers, or a `Makefile` target named `e2e`.
