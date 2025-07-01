from locust import HttpUser, task


class HttpapiUser(HttpUser):
    # httpuser 相关的类的使用
    """
    wait_time = 1
    abstract = True
    @task
    """

    # HttpSession 相关的类的使用
    def test_get(self):
        self.client.get("/")
        self.client.post("/")
        self.client.put("/")
        self.client.delete("/")
        self.client.patch("/")
        self.client.head("/")
        self.client.options("/")

    # 请求相关参数（使用client是相同的参数，除了没有method)
    @task
    def test_get_request(self):
        """
            request_meta = {
            "request_type": method,
            "response_time": response_time,
            "name": name,
            "context": context,
            "response": response,
            "exception": None,
            "start_time": start_time,
            "url": url,
        }
        """
        self.client.request(method="GET", url="/")
        pass

    # 响应验证
    @task
    def test_get2(self):
        """response_meta={
        "_content",
        "status_code",
        "headers",
        "url",
        "history",
        "encoding",
        "reason",
        "cookies",
        "elapsed",
        "request"}
        """
        with self.client.get("/", catch_response=True) as response:
            if response.text != "Success":
                # 使用正确的检查点方法
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.5:
                # 使用正确的检查点方法
                response.failure("Request took too long")


from urllib3 import PoolManager


# 连接池管理
class MyUser(HttpUser):
    # 其主要的功能点的，减少tcp的连接和关闭，以提高性能。
    """
            客户端（请求者）的性能优势
        1.消除连接建立开销
        对于客户端来说，主要的好处是避免了每次请求都需要进行代价高昂的 TCP 三次握手。如果没有连接池，每个 HTTP 请求都需要：

        DNS 解析（如果未缓存）
        TCP连接建立（SYN、SYN-ACK、ACK）
        HTTPS 的 SSL/TLS 握手（多次往返）
        连接池通过重用现有连接来消除这种开销。

        2.降低 SSL/TLS 握手成本
        对于 HTTPS 请求，SSL/TLS 握手尤其昂贵，涉及多次往返和加密操作。连接重用可以避免重复此过程writing-a-locustfile.rst:646。

        3. 更好的资源利用率
        Locust 通过共享连接池证明了这一点。它FastHttpUser可以在多个用户实例之间共享client_pool，从而减少所需的连接总数fasthttp.py:370-371。测试表明，通过允许多个用户共享同一个连接池test_fasthttp.py:604-605 ，可以显著提高性能。

        4.更高的吞吐量
        FastHttpUser 实现具体展示了性能改进，与标准 HttpUser increase-performance.rst:113相比，连接池是实现 4-5 倍更高吞吐量的关键因素。

        服务器（接收器）的性能优势
    1.减少连接管理开销
    服务器受益于更少的新连接请求。每个新的 TCP 连接都需要：

    套接字分配和内存开销
    用于连接处理的进程/线程资源
    操作系统内核资源
    2. 更好的资源配置
    通过连接重用，服务器可以使用相同数量的连接来处理更多请求，从而提高资源效率并允许更高的并发负载处理。

    3.减少上下文切换
    新连接越少，意味着处理新连接建立和服务实际 HTTP 请求之间的上下文切换就越少。

    4. 降低内存占用
    每个 TCP 连接都会消耗服务器内存。连接重用可以减少处理相同请求量所需的并发连接总数。

    客户端和服务器之间影响的主要差异
    客户端优势
    减少延迟：通过避免连接建立时间，客户可以立即看到延迟的改善
    带宽效率：连接建立数据包的网络开销更少
    节省 CPU：通过 SSL 握手重用减少加密操作
    服务器端优势
    可扩展性：可以用相同的资源处理更多的并发客户端
    稳定性：降低高负载下连接耗尽的风险
    资源效率：更好地利用可用的连接槽


    Locust 提供了两种具体的实现，展示了不同的连接池方法：

    带有pool_manager的HttpUser ：允许跨用户实例clients.py:88共享urllib3连接池

    带有 client_pool 的 FastHttpUser：通过共享客户端池提供更高效的实现，以获得更好的性能fasthttp.py:612
    """

    pool_manager = PoolManager(maxsize=10, block=True)
