import io
import base64
import re
from gtts import gTTS


def text_to_speech_base64(text: str, lang: str = "hi") -> str:
    """Convert text to speech and return as base64 audio string"""
    try:
        # Clean text for TTS (remove markdown symbols)
        clean_text = clean_for_tts(text)
        
        # Try Hindi first, fallback to English
        try:
            tts = gTTS(text=clean_text, lang=lang, slow=False)
        except Exception:
            tts = gTTS(text=clean_text, lang="en", slow=False)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Encode to base64
        audio_b64 = base64.b64encode(audio_buffer.read()).decode("utf-8")
        return audio_b64
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def clean_for_tts(text: str) -> str:
    """Remove markdown and special characters for cleaner TTS"""
    # Remove markdown bold/italic
    text = re.sub(r'\*+([^*]+)\*+', r'\1', text)
    # Remove markdown headers
    text = re.sub(r'#{1,6}\s', '', text)
    # Remove bullet points
    text = re.sub(r'^[•\-\*]\s', '', text, flags=re.MULTILINE)
    # Remove numbered lists
    text = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
    # Remove underscore italics
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    # Remove emojis for cleaner speech (optional)
    text = re.sub(r'[^\w\s\.\,\!\?\-\(\)àáâãäåæçèéêëìíîïðñòóôõöùúûüýþÿ\u0900-\u097F]', '', text)
    return text.strip()


def get_audio_html(audio_b64: str) -> str:
    """Generate HTML audio element with autoplay"""
    if not audio_b64:
        return ""
    return f"""
    <audio autoplay style="display:none;">
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    """
