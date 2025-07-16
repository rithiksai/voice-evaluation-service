# app/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
import io
from pydub import AudioSegment
from app.services.stt_service import transcribe_with_assembly
from app.services.analysis_service import (
    compute_pronunciation_score,
    evaluate_pacing,
    detect_pauses,
    generate_feedback_summary
)
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ALLOWED = {"audio/wav", "audio/mpeg"}


@app.post("/transcribe")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED:
        raise HTTPException(415, "Only WAV or MP3 allowed")

    raw = await file.read()
    audio = AudioSegment.from_file(io.BytesIO(raw))
    duration = len(audio) / 1000  # Convert ms to seconds

    if duration > 60:
        raise HTTPException(400, "Audio is greater than 60 s")

    # Step 1: Transcribe
    transcript_json = await transcribe_with_assembly(raw)

    transcript_text = transcript_json["text"]
    words = transcript_json.get("words", [])

    # Step 2: Pronunciation Analysis
    pronunciation_score, mispronounced_words = compute_pronunciation_score(words)

    # Step 3: Pacing Evaluation
    pacing_wpm, pacing_feedback = evaluate_pacing(words, duration)

    # Step 4: Pause Detection
    pause_count, total_pause_time, pause_feedback = detect_pauses(words)

    # Step 5: Generate Natural Language Feedback
    text_feedback = generate_feedback_summary(pacing_feedback, mispronounced_words, pause_feedback)

    formatted_words = [
        {
            "word": w["text"],   # Map 'text' to 'word'
            "start": round(w["start"] / 1000, 3),   # ← Convert to seconds
            "end": round(w["end"] / 1000, 3),  
            "confidence": w["confidence"]
        }
        for w in words
    ]

    # Final Output
    return {
        "filename": file.filename,
        "transcript": transcript_text,
        "words": formatted_words, 
        "audio_duration_sec": duration,
        "pronunciation_score": pronunciation_score,
        "mispronounced_words": mispronounced_words,
        "pacing_wpm": pacing_wpm,
        "pacing_feedback": pacing_feedback,
        "pause_count": pause_count,
        "total_pause_time_sec": total_pause_time,
        "pause_feedback": pause_feedback,
        "text_feedback": text_feedback,
        "assembly_job_id": transcript_json["id"]
    }
