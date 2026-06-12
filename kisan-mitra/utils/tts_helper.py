import re


def clean_for_tts(text: str) -> str:
    """Remove markdown and special characters for cleaner TTS"""
    text = re.sub(r'\*+([^*]+)\*+', r'\1', text)
    text = re.sub(r'#{1,6}\s', '', text)
    text = re.sub(r'^[•\-\*]\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    # Remove emojis
    text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\u0900-\u097F]', '', text)
    return text.strip()


def get_browser_tts_html(text: str, speed: float = 1.0) -> str:
    utterance.rate = """ + str(speed) + """;
    """
    Returns an HTML snippet that uses the browser's Web Speech API
    to speak the given text aloud. No server-side dependencies needed.
    Supports Hindi (hi-IN) for Hinglish responses.
    """
    clean_text = clean_for_tts(text)
    # Escape for JS string
    escaped = clean_text.replace("\\", "\\\\").replace('"', '\\"').replace('\n', ' ')

    return f"""
    <script>
    (function() {{
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance("{escaped}");
        utterance.lang = 'hi-IN';
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        // Try to find a Hindi voice, fallback to default
        const voices = window.speechSynthesis.getVoices();
        const hindiVoice = voices.find(v => v.lang === 'hi-IN' || v.lang.startsWith('hi'));
        if (hindiVoice) utterance.voice = hindiVoice;

        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """
