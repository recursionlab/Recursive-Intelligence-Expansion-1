# 10-Phase Execution Plan - Double-Check (User Runs Commands Manually)

## Pass 1: Implementation

### Phase 1: Core Testing & Validation [READY FOR USER TEST]
- [ ] pytest test_xikernel.py tests/app_test.py --cov=app --cov-report=html (aim 95%+)
- [ ] locust -f tests/load_locust.py --users 100

### Phase 2: Performance Optimization [PROGRESS]
- [x] app.py: Redis cache + /taskboard endpoints
- [x] DB indexes: jobs/workspace_messages

### Phase 3: Security Audit
- [ ] app.py: Full JWT auth, sanitization

### Phase 4: Frontend Refactor
- [ ] frontend/ React Kanban (vite)

### Phase 5-10: [Pending]

## Pass 2: Audit/Validate (Repeat + Fix)

**Self-Fix Progress #1-6 ✓**: run.bat, port 8080, test_deps.py, DB Path, Kernel guard, logging/print.

**Next: #7 Hosts, #8 Firewall netsh, #9 Redis mock.**

Double-click run.bat or start_debug.bat for server + deps check.

Server: http://localhost:8080/health

User: Edit files, then manually: pip install -r requirements.txt && pytest ...
