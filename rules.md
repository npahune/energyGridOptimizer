# EGLO Project Coding & Workflow Standards

## Introduction

These standards guide the EGLO team in building secure, high-quality, and maintainable energy optimization software. We emphasize code quality, security, collaboration, and Behavior-Driven Development (BDD). All development is tracked via GitHub Issues, with automation and traceability as core principles.

---

## 📋 Backlog Management

- Use **GitHub Issues** as the single source of truth for all backlog items (features, bugs, chores).
- Leverage **MCP (Model Context Protocol)** for issue annotation, state tracking, and metadata updates.
- All user stories and tasks must be reflected in GitHub Issues, linked to sprints and epics as per the AgileSprintPlan.md and Backlog.md.

### Workflow

1. **Issue Selection & Annotation**
   - Prioritize by `state: open`, `label: ready`, and business value.
   - Annotate issues with MCP for context and traceability.

2. **Branch Naming Convention**
   - `feature/{issue-number}-{short-title-slug}`
   - `bugfix/{issue-number}-{short-title-slug}`
   - `chore/{issue-number}-{short-title-slug}`

3. **TDD/BDD Workflow**
   - Write failing tests first (pytest for Python).
   - Implement code to pass tests.
   - Refactor for clarity and maintainability.

4. **Pull Request Process**
   - Mark issues as "in progress" when work starts.
   - Open PRs against `develop` branch.
   - Automated checks: linting, security, unit/integration tests.
   - Add MCP comments summarizing coverage and warnings.
   - On merge, update issue to "delivered" and log commit hash.

5. **Issue Closure**
   - Run final integration tests.
   - Mark issue as "closed" if successful.

---

## 📖 Story Types & Estimation

- Classify issues as **Feature**, **Bug**, or **Chore**.
- Use the Fibonacci scale (0, 1, 2, 3, 5, 8) for complexity estimation.
- Reference required API integrations, data model changes, and test coverage in estimates.

---

## 🎨 Coding Style Guidelines

- **Python:** Use PEP 484 type hints for all public functions and classes.
- **Naming:**
  - Database models/entities: `snake_case` for PostgreSQL, `PascalCase` for Python classes.
  - Functions: `snake_case`.
  - Variables: `snake_case`.
- **Formatting:** 4-space indentation, 80-character line limit.
- **Comments:** Use docstrings for all public methods and classes. Remove outdated comments.
- **Imports:** Use absolute imports where possible.
- **Security:** Escape dynamic parameters in queries/templates to prevent injection.

---

## 🧪 Testing Strategy

- Use **pytest** for unit and integration tests.
- Write BDD-style tests for all endpoints and core logic.
- Use in-memory databases or test Supabase projects for integration tests.
- Validate all API routes for status codes, response schemas, and error handling.

---

## 🔄 Continuous Integration & Deployment (CI/CD)

- Use GitHub Actions for CI/CD.
- Pipeline must include: build, lint, unit/integration tests, security scans, and deployment to staging.
- Document and automate remediation for common pipeline failures.

---

## 🗂️ Data & API Standards

- Follow the data model in data_model.md for all schema changes.
- All API endpoints must be documented in OpenAPI/Swagger.
- Use consistent request/response schemas as per prd.md.

---

## 🏷️ Documentation

- Update README.md with setup, usage, and API docs.
- Maintain AgileSprintPlan.md and Backlog.md for sprint and backlog tracking.
- Document all architectural decisions and major changes.

---

These rules ensure the EGLO project remains robust, secure, and easy to maintain as it evolves.
