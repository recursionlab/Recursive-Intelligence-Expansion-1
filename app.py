my
#!/usr/bin/env python3
"""Meta-Theory Building App Backend: ΞKernel API for theory discovery."""
from fastapi import FastAPI, UploadFile, File, Form, Header, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3
from pathlib import Path
import json
from ΞKernel import XiKernel
from typing import List
import re
import jwt
from datetime import datetime, timedelta, timezone
import bleach
SECRET_KEY = "your-secret-key-change-in-prod"
ALGORITHM = "HS256"

app = FastAPI(title="ΞKernel Theory Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init
try:
    kernel = XiKernel()
except Exception:
    class MockKernel:
        def test_triples_loop(self, *args, **kwargs):
            return {"mock": True}
        def _weighted_wolf_call(self, *args, **kwargs):
            return "mock wolf"
    kernel = MockKernel()
DB_PATH = "theory.db"
import redis
import functools
try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.ping()
except:
    from unittest.mock import Mock
    r = Mock(ping=lambda: True, get=lambda k: None, setex=lambda *args: None, delete=lambda k: None)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["name"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS docs (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            title TEXT,
            content TEXT,
            dsrp JSON
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS kanban (
            id INTEGER PRIMARY KEY,
            title TEXT,
            status TEXT DEFAULT 'backlog',
            description TEXT,
            related_docs TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            api_key TEXT PRIMARY KEY,
            name TEXT,
            capabilities JSON
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS workspace_messages (
            id INTEGER PRIMARY KEY,
            agent TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            folder TEXT DEFAULT 'Inbox',
            assigned_to TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_jobs_folder ON jobs (folder)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs (status)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_workspace_messages_agent ON workspace_messages (agent)')
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY,
        agent TEXT,
        action TEXT,
        target_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_audit_agent ON audit_logs (agent)')
    conn.commit()
    conn.close()


init_db()

@app.post("/docs/upload")
async def upload_doc(file: UploadFile = File(...)):
    content = await file.read()
    content_str = content.decode()
    
    # Basic DSRP extraction (heuristic)
    title = re.search(r'^# (.*?)$', content_str, re.M).group(1) if re.search else file.filename
    dsrp = {
        "distinctions": len(re.findall(r'\n[Dd]istinction.*?\n', content_str)),
        "systems": len(re.findall(r'\n[Ss]ystem.*?\n', content_str)),
        "relationships": len(re.findall(r'\n[Rr]elationship.*?\n', content_str)),
        "perspectives": len(re.findall(r'\n[Pp]erspective.*?\n', content_str))
    }
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO docs (path, title, content, dsrp) VALUES (?, ?, ?, ?)",
              (file.filename, title, content_str, json.dumps(dsrp)))
    conn.commit()
    conn.close()
    
    return {"status": "uploaded", "title": title, "dsrp": dsrp}

@app.get("/docs")
async def list_docs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT path, title FROM docs")
    docs = [{"path": row[0], "title": row[1]} for row in c.fetchall()]
    conn.close()
    return docs

@app.post("/chat")
async def chat(query: str = Form(...)):
    # Simple RAG
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM docs LIMIT 3")  # Top 3 docs
    context = "\n".join([row[0][:2000] for row in c.fetchall()])
    conn.close()
    
    # ΞKernel operator chain simulation
    wolf_out = kernel._weighted_wolf_call({"TripleInterp": query}, nx.DiGraph())
    
    return {"response": f"Context: {context[:500]}...\nKernel: {wolf_out}"}

@app.get("/kanban")
async def get_kanban():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM kanban")
    tasks = [{"id": row[0], "title": row[1], "status": row[2], "desc": row[3]} for row in c.fetchall()]
    conn.close()
    return {"tasks": tasks}


@app.post("/kanban/task")
async def add_task(title: str = Form(...), desc: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO kanban (title, description) VALUES (?, ?)", (title, desc))
    conn.commit()
    conn.close()
    return {"status": "task_added"}

@app.post("/register_agent")
async def register_agent(api_key: str = Form(...), name: str = Form(...), capabilities: str = Form(...)):
    api_key = bleach.clean(api_key)
    capabilities = bleach.clean(capabilities)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO agents (api_key, name, capabilities) VALUES (?, ?, ?)",
              (api_key, name, capabilities))
    conn.commit()
    conn.close()
    return {"status": "registered", "name": name}

@app.post("/token")
async def get_token(api_key: str = Form(...)):
    api_key = bleach.clean(api_key)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, capabilities FROM agents WHERE api_key = ?", (api_key,))
    agent = c.fetchone()
    conn.close()
    if not agent:
        return JSONResponse({"error": "invalid api_key"}, 401)
    payload = {
        "name": agent[0],
        "capabilities": json.loads(agent[1]),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

@app.get("/agents")
async def list_agents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, capabilities FROM agents")
    agents = [{"name": row[0], "capabilities": json.loads(row[1])} for row in c.fetchall()]
    conn.close()
    return {"agents": agents}

@app.post("/message")
async def send_message(to_agent: str = Form(...), content: str = Form(...)):
    # Auth
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM agents WHERE api_key = ?", (api_key,))
    sender = c.fetchone()
    if not sender:
        return JSONResponse({"error": "unauthorized"}, 401)
    
    # ΞKernel route + STGemini
    context = kernel.test_triples_loop(1)  # Shared state
    prompt = f"From {sender[0]} to {to_agent}: {content}\nGraph: {json.dumps(context)}"
    
    # Mock LLM for stability (replace with kernel.llm_client in prod)
    response = "Mock STGemini response for " + prompt[:100]
    
    # Log message
    # Log message to workspace_messages
    c.execute("INSERT INTO workspace_messages (agent, content) VALUES (?, ?)",
              (f"{sender[0]}->{to_agent}", content))
    conn.commit()
    conn.close()
    
    return {"response": "Mock response (llm_client mock in prod)", "routed_via": "ΞKernel"}


@app.get("/taskboard")
async def get_taskboard():
    cache_key = "taskboard"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, description, folder, assigned_to FROM jobs")
    jobs = [{"id": row[0], "title": row[1], "description": row[2], "folder": row[3], "assigned_to": row[4]} for row in c.fetchall()]
    
    # Group by folder (MoC)
    moc = {}
    for job in jobs:
        folder = job["folder"]
        if folder not in moc:
            moc[folder] = []
        moc[folder].append(job)
    
    conn.close()
    r.setex(cache_key, 300, json.dumps(moc))  # 5min TTL
    return {"moc": moc}

@app.post("/taskboard/update")
async def update_taskboard(id: int = Form(...), folder: str = Form(...), api_key: str = Form(...)):
    # Auth
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM agents WHERE api_key = ?", (api_key,))
    agent = c.fetchone()
    if not agent:
        conn.close()
        return JSONResponse({"error": "unauthorized"}, 401)
    
    c.execute("UPDATE jobs SET folder = ? WHERE id = ?", (folder, id))
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "job not found"}, 404)
    
    conn.commit()
    r.delete("taskboard")  # Invalidate cache
    conn.close()
    return {"status": "updated", "by": agent[0]}

@app.get("/graph")
async def graph_status():
    # Simple ΞKernel status
    results = kernel.test_triples_loop(1)  # Quick status
    return {"kernel_status": results}

if __name__ == '__main__':
    import uvicorn
    import logging
    logging.basicConfig(level=logging.INFO)
    print("Starting server at http://localhost:8080/health")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

