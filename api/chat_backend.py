import os
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from groq import Groq
from typing import AsyncGenerator
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import aiohttp

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client securely
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=api_key)

async def fetch_docs():
    """Fetch documentation from GitHub repo"""
    async with aiohttp.ClientSession() as session:
        urls = [
            "https://github.com/Ollama-Agent-Roll-Cage/oarc/blob/master/docs/what_is_an_agent/what_is_an_agent.md",
            "https://github.com/Ollama-Agent-Roll-Cage/oarc/tree/master/docs/speech_to_speech",
            "https://github.com/Leoleojames1/agentChef/tree/main/docs"
        ]
        docs = []
        for url in urls:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        docs.append(content)
            except Exception as e:
                print(f"Error fetching {url}: {e}")
        return " ".join(docs)

async def stream_chat_response(message: str) -> AsyncGenerator[str, None]:
    """Stream the chat response from Groq"""
    
    try:
        # Fetch documentation content
        docs = await fetch_docs()
        
        # Create a context-aware prompt
        system_prompt = f"""You are OARC Butler, a helpful AI assistant that explains the OARC (Ollama Agent Roll Cage) documentation.
You have access to the following documentation: {docs[:2000]}...
Always be polite and professional. If you're not sure about something, say so.
Base your responses on the documentation provided."""

        # Create the chat completion
        completion = client.chat.completions.create(
            model="llama2-70b-4096",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=True
        )

        # Stream the response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"I apologize, but I encountered an error: {str(e)}"

@app.post("/api/chat")
async def chat(message: dict):
    """Handle chat messages and return streaming responses"""
    if not message.get("message"):
        raise HTTPException(status_code=400, detail="Message is required")
    return StreamingResponse(
        stream_chat_response(message["message"]),
        media_type="text/event-stream"
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time chat"""
    await websocket.accept()
    
    try:
        while True:
            message = await websocket.receive_text()
            async for response_chunk in stream_chat_response(message):
                await websocket.send_text(response_chunk)
    except Exception as e:
        await websocket.close()