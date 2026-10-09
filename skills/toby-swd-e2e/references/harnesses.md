# End-to-end harnesses

This file lists, for each stack, the files, folders, and markers that a repo's end-to-end setup uses.

- JavaScript: `playwright.config`, `cypress.config`, or `supertest` in a test file
- Python: a `tests/e2e` folder, a pytest marker such as `e2e` or `integration`, or a test that calls Django's `self.client`, DRF's `APIClient`, or pytest-django's `client` fixture
- Go: a test that calls `httptest.NewServer`, or a build tag such as `e2e`
- Ruby: Rails request specs in `spec/requests`, integration tests in `test/integration`, or system tests in `test/system` or `spec/system`
- Mobile: `.detoxrc`, a `.maestro` folder, XCUITest, or Espresso
- Any stack: `docker-compose.test.yml`, testcontainers, or a `Makefile` target named `e2e`
