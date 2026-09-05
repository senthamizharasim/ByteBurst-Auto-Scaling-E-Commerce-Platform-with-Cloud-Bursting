from locust import HttpUser, task, between

class ShopperUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def view_products(self):
        self.client.get("/products")

    @task(1)
    def check_health(self):
        self.client.get("/health")