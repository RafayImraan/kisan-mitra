# 🌾 Kisan Mitra — Voice-Based Natural Farming Consultant

**Connecting Dreams Foundation · Round 2 Technical Assignment · Option B**

> *Har kisan ke haath mein ek jaankaar dost — A knowledgeable friend in every farmer's hands*

---

## 🎯 What It Does

Kisan Mitra is a voice-enabled AI consultant that helps Indian farmers transition to natural/organic farming. Built for a mobile-first, rural Indian audience — it speaks Hinglish, listens to voice commands, and gives instant guidance on:

1. **🔬 Disease Identification & Treatment** — Farmer describes symptoms by voice → AI identifies the disease → suggests organic/natural remedies only
2. **🌦️ Weather & Market Intelligence** — Regional weather forecasts with farming-specific advice + live mandi prices for major crops

---

## 🖥️ Live Demo

> **Deploy URL:** *(add after deploying to Streamlit Community Cloud)*  
> **GitHub Repo:** *(add your repo link)*  
> **Video Walkthrough:** *(add Google Drive / YouTube link)*

---

## 🏗️ Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| **Frontend / UI** | Streamlit | Fast Python-native UI, mobile-friendly, free hosting |
| **AI / LLM** | Claude claude-sonnet-4-6 (Anthropic) | Strong Hindi/Hinglish understanding, strict prompt guardrails |
| **Speech-to-Text (STT)** | Web Speech API (browser-native) | Free, no API key needed, works on Chrome mobile |
| **Text-to-Speech (TTS)** | gTTS (Google Text-to-Speech) | Free, supports Hindi, lightweight |
| **Knowledge Base** | JSON files (farming_knowledge.json) | Lightweight RAG — diseases, remedies, crops, subsidies |
| **Market/Weather Data** | Static JSON (weather_market_data.json) | Realistic dummy data as permitted by assignment |
| **Language** | Python 3.10+ | - |
| **Hosting** | Streamlit Community Cloud | Free live URL |

---

## 🧠 Prompt Design

### System Prompt Strategy

The AI uses **strict guardrails** embedded in the system prompt:

```
LANGUAGE: Always respond in Hinglish (Hindi + English mix).
           Use rural-friendly language — "kisan bhai", "aap", etc.

KNOWLEDGE RULES (STRICT):
- Disease/pest: ONLY organic remedies. NEVER suggest chemicals.
- Fertilizers: ONLY Jeevamrit, Panchagavya, vermicompost, neem cake etc.
- Subsidies: ONLY real govt schemes (PM-KISAN, PKVY, KCC, etc.)
- If unsure: direct farmer to Krishi Vigyan Kendra.
```

### RAG Approach

Instead of a vector database (overkill for this scope), a **structured JSON knowledge base** is injected into the system prompt at runtime:
- `farming_knowledge.json` — 6 diseases with symptoms & organic remedies, 4 crop profiles, 5 govt subsidies, Jeevamrit recipe
- `weather_market_data.json` — 5 regional weather forecasts, 9 crop market prices

This gives the model grounded, accurate information while the guardrails prevent hallucination of chemical advice or fake schemes.

---

## 🌍 Localization

| Feature | Implementation |
|---------|---------------|
| **Language** | Hinglish (Hindi + English mix) in all AI responses |
| **Script** | Devanagari labels in UI headers and buttons |
| **Voice Input** | Hindi-IN locale (`hi-IN`) in Web Speech API |
| **Voice Output** | gTTS with `lang='hi'` for Hindi TTS |
| **Crops/Diseases** | Both Hindi and English names in knowledge base |
| **Subsidy Names** | Official Hindi names used (e.g., Paramparagat Krishi Vikas Yojana) |
| **Friendly tone** | "Kisan bhai", "aap", "namaste" — rural Indian register |

---

## 📁 Project Structure

```
kisan-mitra/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   ├── config.toml                 # Theme and server config
│   └── secrets.toml                # API keys (DO NOT commit)
├── data/
│   ├── farming_knowledge.json      # Disease, crop, subsidy knowledge base
│   └── weather_market_data.json    # Regional weather + mandi price data
└── utils/
    ├── __init__.py
    ├── ai_helper.py                # Claude API calls + prompt engineering
    └── tts_helper.py               # gTTS text-to-speech utility
```

---

## 🚀 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/kisan-mitra.git
cd kisan-mitra
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key

Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

Or set as environment variable:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 4. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in Chrome (for voice support).

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (make sure `secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** → `app.py`
5. Under **Advanced settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "your-key-here"
   ```
6. Click **Deploy** — live URL in ~2 minutes ✅

---

## 🎥 Features Walkthrough

### Feature 1 — Disease Identification & Treatment
- Farmer taps mic button, says: *"Mere tamatar ke patte par safed daag aa rahe hain"*
- Web Speech API converts voice → text (Hindi-IN)
- Text sent to Claude with farming knowledge base injected
- Claude identifies Powdery Mildew, gives organic neem-based remedy in Hinglish
- gTTS reads the response aloud in Hindi

### Feature 2 — Weather & Market Intelligence
- Farmer selects their region from sidebar (Punjab, Haryana, UP, Maharashtra, Rajasthan)
- Live weather card shows temperature, forecast, rain chance
- Market price panel shows today's mandi rates for 9 major crops with MSP comparison
- Farmer can ask voice questions like *"Aaj gehu ki kimat kya hai?"*

### Quick Questions
- Pre-built buttons for instant answers: Mausam, Mandi Bhav, Jeevamrit recipe

---

## 📊 Evaluation Criteria Mapping

| Criterion | Weight | How We Address It |
|-----------|--------|-------------------|
| **Technical** | 40% | Full STT/TTS pipeline, deployed Streamlit app, Claude API integration, JSON-based RAG |
| **Empathy / UX** | 30% | Hinglish voice interface, mobile-first layout, quick buttons for low-literacy users, warm conversational tone |
| **AI / Prompt** | 30% | Strict organic-only guardrails, knowledge base injection, Hinglish language instruction, hallucination prevention |

---

## ⚠️ Known Limitations

- Voice input requires **Chrome browser** (Web Speech API not supported in Firefox/Safari)
- Weather and market data is **sample/dummy data** (as permitted by CDF assignment)
- TTS quality for Hinglish is good but not perfect — purely Hindi responses sound more natural
- Knowledge base covers common crops/diseases; rare queries go to KVK recommendation

---

## 🌱 Future Improvements

- [ ] Real weather API (OpenWeatherMap) integration
- [ ] Live mandi prices via Agmarknet / data.gov.in API
- [ ] Larger RAG knowledge base with PDF ingestion
- [ ] WhatsApp integration for even lower friction
- [ ] Offline mode for areas with poor connectivity
- [ ] Support for more regional languages (Punjabi, Marathi, Telugu)

---

*Built with ❤️ for India's farmers · Connecting Dreams Foundation · June 2025*
