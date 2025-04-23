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

from web_crawler import WebCrawler

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

# Initialize WebCrawler
crawler = WebCrawler()

async def stream_chat_response(message: str) -> AsyncGenerator[str, None]:
    """Stream the chat response from Groq"""
    
    # First, let's get relevant documentation using the webcrawler
    try:
        # Crawl the documentation pages
        docs = await crawler.crawl_documentation_site("https://github.com/Ollama-Agent-Roll-Cage/oarc/tree/master/docs")
        
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