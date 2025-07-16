def compute_pronunciation_score(words: list, threshold: float = 0.85):
    if not words:
        return 0, []

    confidences = [w["confidence"] for w in words]
    avg_confidence = sum(confidences) / len(confidences)
    pronunciation_score = round(avg_confidence * 100)

    mispronounced_words = [
        {
            "word": w["text"],   
            "start": round(w["start"] / 1000, 3),
            "confidence": w["confidence"]
        }
        for w in words if w["confidence"] < threshold
    ]

    return pronunciation_score, mispronounced_words



def evaluate_pacing(words: list, duration_sec: float):
    """
    Calculate words per minute and pacing feedback.
    """
    word_count = len(words)
    wpm = (word_count / duration_sec) * 60 if duration_sec > 0 else 0
    wpm = round(wpm)

    if wpm < 90:
        feedback = "Too slow"
    elif wpm > 150:
        feedback = "Too fast"
    else:
        feedback = "Your speaking pace is appropriate."

    return wpm, feedback


def detect_pauses(words: list, pause_threshold: float = 0.5):
    """
    Detect significant pauses between words (> 0.5 sec).
    """
    pause_count = 0
    total_pause_time = 0.0

    for i in range(len(words) - 1):
        current_end = words[i]["end"] / 1000   # Convert to sec
        next_start = words[i + 1]["start"] / 1000   # Convert to sec
        gap = next_start - current_end

        if gap > pause_threshold:
            pause_count += 1
            total_pause_time += gap

    pause_feedback = "Try to reduce long pauses to improve fluency." if pause_count > 0 else "No significant pauses detected."

    return pause_count, round(total_pause_time, 2), pause_feedback



def generate_feedback_summary(pacing_feedback, mispronounced_words, pause_feedback):
    """
    Create a natural language feedback summary.
    """
    mispronounced_list = [w["word"] for w in mispronounced_words]
    if mispronounced_list:
        mispronounced_str = ", ".join(mispronounced_list)
        pronunciation_part = f"Focus on pronouncing '{mispronounced_str}' more clearly."
    else:
        pronunciation_part = "Your pronunciation was clear."

    summary = f"{pacing_feedback} {pronunciation_part} {pause_feedback}"

    return summary
