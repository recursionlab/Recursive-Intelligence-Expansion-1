try:
    from fastapi import FastAPI
    import uvicorn
    import sqlite3
    import redis
    from ΞKernel import XiKernel
    import jwt
    import bleach
    print("All deps OK")
except ImportError as e:
    print(f"Missing: {e}")
