# 10 Iterative Debugging Prompts for ΞKernel Taskboard

1. **Lint & Static Analysis**: `pylint **/*.py`, `mypy .`, `black . --check`. Fix errors, add types, bandit security scan.

2. **Dep Audit**: `pip-audit`, `pip freeze > locked-reqs.txt`. Test upgrades.

3. **Runtime Logs**: `uvicorn app:app --reload --log-level debug`. Curl all endpoints, fix exceptions/imports.

4. **DB Validation**: `sqlite3 theory.db ".schema"`, add constraints. Alembic migration stub.

5. **Test CI**: `pytest -v --cov-fail-under=90`. GitHub Actions yaml.

6. **Load/Sec Stress**: `locust -u 200`, OWASP ZAP localhost:8000. Rate-limit.

7. **Unicode Audit**: Grep unicode, test encoding volumes/. Python3.11 verify.

8. **E2E Frontend**: Playwright test taskboard flow. Screenshot.

9. **Profile Memory**: memray uvicorn 1hr. Prune cron.

10. **Fuzz Chaos**: Hypothesis DB fuzz. Docker kill tests.

Run sequentially, update TODO.md.
