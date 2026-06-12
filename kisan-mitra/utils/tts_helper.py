import re


def clean_for_tts(text: str) -> str:
    text = re.sub(r'\*+([^*]+)\*+', r'\1', text)
    text = re.sub(r'#{1,6}\s', '', text)
    text = re.sub(r'^[•\-\*]\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\u0900-\u097F]', '', text)
    return text.strip()


def get_browser_tts_html(text: str, speed: float = 1.0) -> str:
    clean_text = clean_for_tts(text)
    escaped = clean_text.replace("\\", "\\\\").replace('"', '\\"').replace('\n', ' ')
    speed_val = float(speed)

    html = """
    <script>
    (function() {
        window.speechSynthesis.cancel();
        var utterance = new SpeechSynthesisUtterance(\"""" + escaped + """\");
        utterance.lang = 'hi-IN';
        utterance.rate = """ + str(speed_val) + """;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        var voices = window.speechSynthesis.getVoices();
        var hindiVoice = voices.find(function(v) { return v.lang === 'hi-IN' || v.lang.startsWith('hi'); });
        if (hindiVoice) utterance.voice = hindiVoice;
        window.speechSynthesis.speak(utterance);
    })();
    </script>
    """
    return html