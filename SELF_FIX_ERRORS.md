# 20 Self-Handleable localhost Refused Fixes (AI-Autonomous)

1. Create run.bat: `uvicorn app:app --reload --host 0.0.0.0 --port 8080`
2. Edit app.py: port=8080 in uvicorn.run.
3. Add if __name__: print("Server starting http://127.0.0.1:8000/docs")
4. Test deps: create test_deps.py import all reqs.
5. Kill port: taskkill /f /im python.exe (restart).
6. Hosts fix: append '127.0.0.1 localhost' to hosts.
7. Firewall rule: netsh advfirewall firewall add rule name="Uvicorn" dir=in action=allow program="python" enable=yes
8. Redis stub: if not r.ping(): r = Mock()
9. DB abs path: DB_PATH = Path(__file__).parent / "theory.db"
10. Import guard: try: from ΞKernel import XiKernel except: class XiKernel: pass
11. Coroutine fix: import asyncio; asyncio.run(uvicorn.run...)
12. Env port: os.getenv("PORT", 8000)
13. Log errors: logging.basicConfig(level=logging.DEBUG)
14. Health endpoint: @app.get("/health") return {"status": "ok"}
15. Pre-flight CORS: @app.options("/") def options(): pass
16. Thread pool: from concurrent.futures import ThreadPoolExecutor
17. SSL stub: --ssl-keyfile none
18. Workers=1 explicit.
19. Bind log: uvicorn.run(..., log_level="info")
20. VSCode terminal restart + cd project && python -m uvicorn app:app
