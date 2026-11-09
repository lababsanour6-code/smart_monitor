import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
app = FastAPI()

class ChatRequest(BaseModel):
    messages: list[dict]
    cpu: float = 0
    ram: float = 0
    disk: float = 0

@app.post("/api/chat")
def chat(data: ChatRequest):
    try:
        messages = [
            m for m in data.messages[-16:]
            if m.get("role") in ("user", "assistant")
            and isinstance(m.get("content"), str)
            and m["content"].strip()
        ]

        if not messages or messages[-1]["role"] != "user":
            raise HTTPException(400, "Invalid question")

        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=900,
            system=(
                "You are a computer assistant. Help with Linux, "
                "Ubuntu, hardware, CPU, RAM, disk, networking, "
                "Python and troubleshooting. Reply in the user's "
                "language. Current readings: "
                f"CPU={data.cpu}%, RAM={data.ram}%, "
                f"Disk={data.disk}%."
            ),
            messages=messages
        )

        reply = "".join(
            x.text for x in response.content
            if getattr(x, "type", "") == "text"
        )
        return {"reply": reply}

    except HTTPException:
        raise
    except Exception as error:
        print("AI ERROR:", repr(error))
        raise HTTPException(500, "AI service error")