class Server:
    def __init__(self, env):
        self.app = {
            "dev": "http://127.0.0.1:8002",
            "beta": "http://127.0.0.1:8002",
            "rc": "http://127.0.0.1:8002",
        }[env]
