from locust import task,User

# user类学习
# abstract = True 用于把 User 类标记为抽象类，Locust 不会执行该类。
# 抽象类可用于定义通用的行为和属性，供其他具体的 User 子类继承。
class TestUser(User):
    #包含的基础属性 
    fixed_count = 1
    weight = 1
    constant = 1000
    constant_throughput = 1
    constant_pacing = 1


    between = 1, 2
    wait_time = between
    host = "http://localhost:8080"

    
    def on_start(self):
        print("开始")

    @task
    def test_get(self):
        # 可直接通过self访问属性
        print(f"测试类{self.host,self.wait_time,self.abstract,self.fixed_count,self.weight,self.constant,self.constant_throughput,self.constant_pacing}")
    
    
    def on_stop(self):
        print("结束")