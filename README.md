# 🎙️ Voice Evaluation Microservice

## 🧪 **Assignment:** AI-Powered Go-To-Market Strategy & Content Package – **Voice Feedback Microservice**

### **Objective**

Build a microservice that processes spoken answers and provides structured feedback on:

- **Pronunciation**
- **Pacing (WPM)**
- **Pause Detection**
- **Natural Language Feedback**

---

## 🚀 **Features**

- Upload `.wav` or `.mp3` audio (≤ 60 seconds)
- Get detailed feedback including:
  - Transcript with word-level metadata (timestamps, confidence)
  - Pronunciation score + mispronounced words
  - Speech pacing (words per minute)
  - Pause pattern detection (count + total pause time)
  - Natural language feedback summary

---

## 📦 **Tech Stack**

- **Python** (FastAPI)
- **AssemblyAI** (for transcription + word-level metadata)
- **Pydub** (for audio duration validation)
- **httpx** (async HTTP client)

---

## ⚙️ **Setup Instructions**

1️⃣ **Clone the Repo**

```bash
git clone https://github.com/your-username/voice-evaluation-service.git
cd voice-evaluation-service
```

2️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

3️⃣ **Create `.env` file**

```env
ASSEMBLY_KEY=sk_live_your_assemblyai_key
```

4️⃣ **Run the App**

```bash
uvicorn app.main:app --reload
```

---

## 🎯 **API Usage**

### **Endpoint:**

`POST /transcribe`

### **Request:**

- **File** (form-data): `.wav` or `.mp3` file ≤ 60 seconds

### **Response:**

```json
{
  "filename": "Recording.mp3",
  "transcript": "Hello my name is Arjun.",
  "words": [
    { "word": "Hello", "start": 0.0, "end": 0.25, "confidence": 0.91 },
    { "word": "my", "start": 0.26, "end": 0.35, "confidence": 0.95 }
  ],
  "audio_duration_sec": 8.2,
  "pronunciation_score": 82,
  "mispronounced_words": [
    { "word": "Arjun", "start": 1.4, "confidence": 0.71 }
  ],
  "pacing_wpm": 104,
  "pacing_feedback": "Your speaking pace is appropriate.",
  "pause_count": 3,
  "total_pause_time_sec": 2.6,
  "pause_feedback": "Try to reduce long pauses to improve fluency.",
  "text_feedback": "You spoke at a good pace. Focus on pronouncing 'Arjun' more clearly. Try to reduce long pauses."
}
```

---

## 🧪 **Test with `curl`**

```bash
curl -X POST "http://127.0.0.1:8000/transcribe"   -H  "accept: application/json"   -H  "Content-Type: multipart/form-data"   -F "file=@sample_audio.wav"
```

---

## 📁 **Project Structure**

```
app/
 ├── main.py               # FastAPI endpoint
 └── services/
       ├── stt_service.py  # AssemblyAI transcription logic
       └── analysis_service.py # Pronunciation, pacing, pauses
.env                        # API keys
requirements.txt            # Python dependencies
```

---

## 🎧 **Sample Audio**

sample audio file used - `intro.mp3` in the repository.

---

## 📝 **Assumptions & Notes**

- Pause threshold: **0.5 seconds**
- Mispronunciation threshold: **confidence < 0.85**
- Word timings are **converted to seconds** from AssemblyAI’s millisecond output.

---

## 💌 **Made with love by**

**Rithik Sai Motupalli**  
📧 **rithikmotupalli@gmail.com**
