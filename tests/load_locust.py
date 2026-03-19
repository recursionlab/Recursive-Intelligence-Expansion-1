from locust import HttpUser, task, between

class TaskboardUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_taskboard(self):
        self.client.get("/kanban")

    @task(2)
    def chat(self):
        self.client.post("/chat", json={"query": "load test"})

    @task(1)
    def register_agent(self):
        self.client.post("/register_agent", json={
            "api_key": "loadkey",
            "name": "LoadBot",
            "capabilities": ["test"]
        })

# Run: locust -f tests/load_locust.py --headless -u 100 -r 10
