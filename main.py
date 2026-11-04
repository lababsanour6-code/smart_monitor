import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(title="Smart Server AI", version="1.0.0")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

client = genai.Client(api_key=API_KEY) if API_KEY else None


class ChatRequest(BaseModel):
    messages: list[dict[str, Any]] = Field(default_factory=list)
    cpu: Any = None
    ram: Any = None
    disk: Any = None


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Smart Server AI"}


@app.post("/v1/chat")
def chat(payload: ChatRequest):
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY is not configured on the server."
        )

    if not payload.messages:
        raise HTTPException(status_code=400, detail="No messages were provided.")

    contents = []
    for item in payload.messages[-20:]:
        role = str(item.get("role", "user")).lower()
        text = item.get("content", item.get("text", ""))

        if not isinstance(text, str) or not text.strip():
            continue

        if role in ("assistant", "model"):
            gemini_role = "model"
        elif role in ("user",):
            gemini_role = "user"
        else:
            continue

        contents.append(
            types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=text[:12000])]
            )
        )

    if not contents:
        raise HTTPException(status_code=400, detail="No usable text messages.")

    system_context = (
        "You are the AI assistant inside a smart server monitoring application. "
        "Answer clearly and safely. Do not claim to have executed commands or "
        "changed a server. Explain any proposed server command before suggesting it.\n"
        f"Current monitoring values: CPU={payload.cpu}, "
        f"RAM={payload.ram}, Disk={payload.disk}.\n"
        "Use these values as context only; if a value is missing, say so."
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_context,
                temperature=0.4,
                max_output_tokens=1200,
            ),
        )
        reply = response.text
        if not reply:
            raise RuntimeError("Gemini returned an empty response.")
        return {"reply": reply}
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini request failed: {str(exc)[:500]}"
        ) from exc
