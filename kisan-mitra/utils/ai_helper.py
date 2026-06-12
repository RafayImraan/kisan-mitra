import json
import os
import requests
from pathlib import Path

# Load knowledge base
DATA_DIR = Path(__file__).parent.parent / "data"

def load_knowledge_base():
    with open(DATA_DIR / "farming_knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_weather_market():
    with open(DATA_DIR / "weather_market_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

KNOWLEDGE_BASE = load_knowledge_base()
WEATHER_MARKET = load_weather_market()

SYSTEM_PROMPT = """You are Kisan Mitra — a friendly, knowledgeable natural farming consultant for Indian farmers.

ROLE: Help farmers with disease identification, organic remedies, weather info, and market prices.

LANGUAGE: Always respond in Hinglish (mix of Hindi and English). Use simple, rural-friendly language that a farmer can easily understand. Use words like "bhai", "kisan bhai", "aap", etc. Keep it warm and friendly.

KNOWLEDGE RULES (STRICT):
- For disease/pest problems: ONLY recommend organic and natural remedies. Never suggest chemical pesticides.
- For fertilizers: ONLY recommend organic options (Jeevamrit, Panchagavya, vermicompost, neem cake, etc.)
- For subsidies: Only mention real government schemes (PM-KISAN, PKVY, KCC, etc.)
- Do NOT make up prices, statistics, or government schemes.
- If you don't know something, say "Mujhe is baare mein pakki jaankari nahi hai, aap apne Krishi Vigyan Kendra se poochh sakte hain."

CONTEXT DATA:
You have access to the following farming knowledge base:

DISEASES & REMEDIES:
{diseases}

CROP INFORMATION:
{crops}

GOVERNMENT SUBSIDIES:
{subsidies}

JEEVAMRIT RECIPE:
{jeevamrit}

WEATHER DATA (Dummy/Sample):
{weather}

MARKET PRICES (Sample):
{market_prices}

RESPONSE FORMAT:
- Keep responses concise (3-5 sentences max for simple questions)
- Use bullet points for remedies/steps
- Always end with an encouraging word for the farmer
- For weather: mention farming implications
- For diseases: always give prevention tips too

IMPORTANT: You are a natural farming specialist. Always promote sustainable, chemical-free farming."""


def get_api_key():
    """Get Gemini API key from Streamlit secrets or environment variable"""
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")


def get_ai_response(user_query: str, conversation_history: list = None) -> str:
    """Get AI response from Gemini API"""

    # Prepare knowledge context
    diseases_text = json.dumps(KNOWLEDGE_BASE["diseases"], ensure_ascii=False, indent=2)
    crops_text = json.dumps(KNOWLEDGE_BASE["crops"], ensure_ascii=False, indent=2)
    subsidies_text = json.dumps(KNOWLEDGE_BASE["subsidies"], ensure_ascii=False, indent=2)
    jeevamrit_text = json.dumps(KNOWLEDGE_BASE["jeevamrit_recipe"], ensure_ascii=False, indent=2)
    weather_text = json.dumps(WEATHER_MARKET["weather"], ensure_ascii=False, indent=2)
    market_text = json.dumps(WEATHER_MARKET["market_prices"], ensure_ascii=False, indent=2)

    system = SYSTEM_PROMPT.format(
        diseases=diseases_text,
        crops=crops_text,
        subsidies=subsidies_text,
        jeevamrit=jeevamrit_text,
        weather=weather_text,
        market_prices=market_text
    )

    # Build Gemini-format contents list
    contents = []

    # Add conversation history
    if conversation_history:
        for msg in conversation_history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Add current user message
    contents.append({"role": "user", "parts": [{"text": user_query}]})

    api_key = get_api_key()
    if not api_key:
        return "❌ API key nahi mila. Streamlit secrets mein GEMINI_API_KEY add karein."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"

    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {
            "maxOutputTokens": 1024,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.Timeout:
        return "⏳ Response time out ho gaya. Dobara try karein, kisan bhai."
    except Exception as e:
        return f"❌ Kuch gadbad ho gayi: {str(e)}. Thodi der baad try karein."


def get_quick_disease_info(symptoms: str) -> dict:
    """Quick lookup for disease based on symptoms keywords"""
    symptoms_lower = symptoms.lower()
    matches = []

    for disease in KNOWLEDGE_BASE["diseases"]:
        for symptom in disease["symptoms"]:
            if any(word in symptoms_lower for word in symptom.lower().split()):
                matches.append(disease)
                break

    return matches[:2] if matches else []


def get_market_summary() -> str:
    """Get formatted market price summary"""
    prices = WEATHER_MARKET["market_prices"]["crops"]
    summary = "📊 **Aaj ke Mandi Bhav** (Rs/quintal)\n\n"

    for crop in prices:
        trend_emoji = "📈" if crop["trend"] == "up" else ("📉" if crop["trend"] == "down" else "➡️")
        summary += f"{trend_emoji} **{crop['name']}**: ₹{crop['market_price']:,}"
        if crop.get("msp"):
            summary += f" (MSP: ₹{crop['msp']:,})"
        summary += f" {crop['change']}\n"

    summary += f"\n_Data: {WEATHER_MARKET['market_prices']['last_updated']}_"
    return summary


def get_weather_summary(region: str = "punjab") -> str:
    """Get weather summary for a region"""
    region_key = region.lower().replace(" ", "_")

    weather_data = WEATHER_MARKET["weather"]
    matched = None

    for key, data in weather_data.items():
        if region_key in key or key in region_key or region.lower() in data["region"].lower():
            matched = data
            break

    if not matched:
        matched = weather_data["punjab"]  # default

    w = matched["current"]
    forecast = matched["forecast"]

    summary = f"🌤️ **{matched['region']} ka Mausam**\n\n"
    summary += f"**Abhi:** {w['temp_celsius']}°C, {w['condition']}\n"
    summary += f"Humidity: {w['humidity']}% | Barish chance: {w['rain_chance']}%\n\n"
    summary += "**Agli 3 din:**\n"

    for day in forecast:
        summary += f"• {day['day']}: {day['high']}°C/{day['low']}°C — {day['condition']} ({day['rain']} barish)\n"

    summary += f"\n🌾 **Khet Salah:** {matched['farming_advice']}"
    return summary
