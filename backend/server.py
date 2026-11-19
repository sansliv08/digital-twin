from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
import json
import uuid
from datetime import datetime
from context import prompt

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize OpenAI client (via OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

# Memory storage configuration
MEMORY_DIR = os.getenv("MEMORY_DIR", "/app/memory")


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class Message(BaseModel):
    role: str
    content: str
    timestamp: str


# Memory management functions
def get_memory_path(session_id: str) -> str:
    return os.path.join(MEMORY_DIR, f"{session_id}.json")


def load_conversation(session_id: str) -> List[Dict]:
    """Load conversation history from local storage"""
    file_path = get_memory_path(session_id)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_conversation(session_id: str, messages: List[Dict]):
    """Save conversation history to local storage"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    file_path = get_memory_path(session_id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


@app.get("/")
async def root():
    return {
        "message": "AI Digital Twin API",
        "memory_enabled": True,
        "storage": "local",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        conversation = load_conversation(session_id)

        messages = [{"role": "system", "content": prompt()}]

        # Keep last 10 messages for context window
        for msg in conversation[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": request.message})

        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
        )

        assistant_response = response.choices[0].message.content
        now = datetime.now().isoformat()

        conversation.append(
            {"role": "user", "content": request.message, "timestamp": now}
        )
        conversation.append(
            {"role": "assistant", "content": assistant_response, "timestamp": now}
        )

        save_conversation(session_id, conversation)

        return ChatResponse(response=assistant_response, session_id=session_id)

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Retrieve conversation history"""
    try:
        conversation = load_conversation(session_id)
        return {"session_id": session_id, "messages": conversation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)