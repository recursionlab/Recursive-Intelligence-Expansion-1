 mimport pytest
from fastapi.testclient import TestClient
from app import app, init_db
from unittest.mock import Mock, patch
import sqlite3
import os

client = TestClient(app)

DB_PATH = "theory.db"

def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

@pytest.fixture(autouse=True)
def reset_db():
    setup_db()

def test_upload_doc():
    with open("test_doc.md", "w") as f:
        f.write("# Test\\nContent")
    with open("test_doc.md", "rb") as f:
        response = client.post("/docs/upload", files={"file": ("test_doc.md", f, "text/markdown")})
    assert response.status_code == 200
    assert "title" in response.json()
    os.remove("test_doc.md")

@patch('app.kernel')
def test_chat(mock_kernel):
    mock_kernel._weighted_wolf_call.return_value = "mock wolf"
    response = client.post("/chat", data={"query": "test"})
    assert response.status_code == 200
    assert "Kernel" in response.json()["response"]

def test_taskboard_get():
    response = client.get("/taskboard")
    assert response.status_code == 200
    assert "moc" in response.json()

def test_kanban_get():
    response = client.get("/kanban")
    assert response.status_code == 200
    assert "tasks" in response.json()

def test_register_agent():
    response = client.post("/register_agent", data={
        "api_key": "testkey",
        "name": "TestAgent",
        "capabilities": '["theory"]'
    })
    assert response.status_code == 200

def test_message_auth():
    # Register first
    client.post("/register_agent", data={"api_key": "testkey", "name": "Test", "capabilities": "[]"})
    response = client.post("/message", data={
        "to_agent": "other",
        "content": "hi",
        "api_key": "testkey"
    })
    assert response.status_code == 200

def test_message_unauth():
    response = client.post("/message", data={"to_agent": "other", "content": "hi", "api_key": "bad"})
    assert response.status_code == 401

# Phase 1 Validation
def test_db_schema():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    expected = ['docs', 'kanban', 'agents', 'workspace_messages', 'jobs']
    assert all(t in tables for t in expected)
