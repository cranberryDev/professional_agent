from dotenv import load_dotenv
import getpass
import os
import uuid
from fastapi import FastAPI
from fastapi.responses import FileResponse
from agent import get_agent_response
from main_functions import ChatRequest
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from session_redis import SessionManager  # Make sure this import matches your file/module name

load_dotenv()
# if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
#     os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_mgr = SessionManager()

@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")

@app.get("/")
def server_root():
    return {"message": "Hello, FastAPI is running!"}

@app.get("/redis-health")
def redis_health():
    try:
        # PING returns True if Redis is connected
        if session_mgr.client.ping():
            return {"redis": "connected"}
        else:
            return {"redis": "not connected"}
    except Exception as e:
        return {"redis": "not connected", "error": str(e)}

@app.post("/chatagent")
def chat_agent(request: ChatRequest):
    print("inside chat agent")
    session_id = request.session_id or str(uuid.uuid4())

    # Check if session exists in Redis
    if session_mgr.session_exists(session_id):
        # Append user message to existing session
        session_mgr.add_message(session_id, "user", request.userchat)
    else:
        # Create new session and add user message
        session_mgr.create_session(session_id)
        session_mgr.add_message(session_id, "user", request.userchat)

    response = get_agent_response(user_input=request.userchat)
    session_mgr.add_message(session_id, "agent", response)

    return {"response": response, "session_id": session_id}
