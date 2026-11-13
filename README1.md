# Smart Server AI backend

This is the small web backend used by the Smart Server Monitoring client.

## Environment variables

- `GEMINI_API_KEY` — set this in the hosting provider's secret/environment settings. Never commit it to GitHub.
- `GEMINI_MODEL` — optional; defaults to `gemini-flash-latest`.

## Render settings

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

The health endpoint is `/`. The chat endpoint is `POST /v1/chat`.

## Request format

```json
{
  "messages": [{"role": "user", "content": "Hello"}],
  "cpu": 12.5,
  "ram": 40.0,
  "disk": 62.0
}
```

The response format is:

```json
{"reply": "Hello! How can I help?"}
```

Before making this service publicly available, add proper authentication, rate limiting,
usage monitoring, and abuse protection. A private GitHub repository does not protect
a publicly deployed web endpoint.
