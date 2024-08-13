
from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def predict(self):
        self.client.post("/predict", json={"data": "sample data"})

    @task
    def health_check(self):
        self.client.get("/health")
