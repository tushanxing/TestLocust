from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task   #标识当前def为可执行的测试
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")