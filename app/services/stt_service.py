"""
AssemblyAI async helper – upload, request, poll, and return the
final transcript JSON (includes `text`, `words`, `id`, etc.).

Reads your AssemblyAI key from the environment:
    ASSEMBLY_KEY=sk_live_...

Install deps:
    pip install httpx python-dotenv
"""

import asyncio
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
load_dotenv()  # Ensure .env vars are loaded

import httpx

# ------------------------------------------------------------------
# 1 – Config / constants
# ------------------------------------------------------------------
AUDIO_CHUNK = 5_242_880                # 5 MB per chunk
BASE_URL    = "https://api.assemblyai.com/v2"
API_KEY     = os.getenv("ASSEMBLY_KEY")  # load_dotenv() should run in main.py

if not API_KEY:
    raise RuntimeError(
        "ASSEMBLY_KEY missing – set it in .env or export it "
        "in your shell before starting the service."
    )

HEADERS = {"authorization": API_KEY}


# ------------------------------------------------------------------
# 2 – Internal helpers
# ------------------------------------------------------------------
async def _byte_stream(data: bytes) -> AsyncGenerator[bytes, None]:
    """Yield the audio bytes in 5 MB chunks so httpx can stream them."""
    for i in range(0, len(data), AUDIO_CHUNK):
        yield data[i : i + AUDIO_CHUNK]


async def _upload(data: bytes, client: httpx.AsyncClient) -> str:
    """POST /upload and return the resulting `upload_url`."""
    resp = await client.post(
        f"{BASE_URL}/upload",
        headers=HEADERS,
        data=_byte_stream(data),
    )
    resp.raise_for_status()
    return resp.json()["upload_url"]


async def _request(audio_url: str, client: httpx.AsyncClient) -> str:
    """Start a transcription job and return its ID."""
    resp = await client.post(
        f"{BASE_URL}/transcript",
        headers=HEADERS,
        json={
            "audio_url": audio_url,
            "punctuate": True,
            "format_text": True,
            # word-level timestamps & confidences are on by default
        },
    )
    resp.raise_for_status()
    return resp.json()["id"]


async def _poll(tid: str, client: httpx.AsyncClient) -> dict:
    """Poll every 2 s until AssemblyAI reports `completed`."""
    url = f"{BASE_URL}/transcript/{tid}"
    while True:
        poll = await client.get(url, headers=HEADERS)
        poll.raise_for_status()
        data = poll.json()
        status = data["status"]
        if status == "completed":
            return data
        if status == "error":
            raise RuntimeError(f"AssemblyAI error: {data['error']}")
        await asyncio.sleep(2)


# ------------------------------------------------------------------
# 3 – Public API
# ------------------------------------------------------------------
async def transcribe_with_assembly(data: bytes) -> dict:
    """
    High-level helper: feed raw audio bytes, get the final JSON back.

    Usage:
        transcript_json = await transcribe_with_assembly(raw_bytes)
    """
    async with httpx.AsyncClient(timeout=None) as client:
        audio_url = await _upload(data, client)
        tid       = await _request(audio_url, client)
        result    = await _poll(tid, client)
    return result
