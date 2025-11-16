import redis
import os
from dotenv import load_dotenv  

load_dotenv()

class SessionManager:
    def __init__(self, host=os.getenv("REDIS_HOST"), port=18542,  expiry_seconds=120):
        self.client = redis.Redis(host=host,
                                  port=port,username="default",
                                  password=os.getenv("REDIS_PASSWORD") 
                                  ,decode_responses=True, ssl=True,ssl_cert_reqs=None,
                                  ssl_check_hostname=False  )
        print(self.client, "Redis client initialized")
        self.expiry_seconds = expiry_seconds

    def session_exists(self, session_id: str) -> bool:
        return self.client.exists(f"session:{session_id}")

    def create_session(self, session_id: str):
        # Optionally initialize session metadata here
        self.client.rpush(f"session:{session_id}", "Session started")
        self.client.expire(session_id, self.expiry_seconds)

    def add_message(self, session_id: str, sender: str, message: str):
        self.client.rpush(f"session:{session_id}", f"{sender}: {message}")
        self.client.expire(session_id, self.expiry_seconds)

    def get_session_messages(self, session_id: str):
        return self.client.lrange(f"session:{session_id}", 0, -1)