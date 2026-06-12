import streamlit as st
import sys
import os
from pathlib import Path
import streamlit.components.v1 as components
# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.ai_helper import get_ai_response, get_market_summary, get_weather_summary
from utils.tts_helper import get_browser_tts_html

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kisan Mitra — प्राकृतिक खेती सलाहकार",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Mukta:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

    /* Root theme */
    :root {
        --green-dark:   #1a4731;
        --green-mid:    #2d6a4f;
        --green-light:  #52b788;
        --green-pale:   #d8f3dc;
        --earth-brown:  #8b4513;
        --earth-light:  #deb887;
        --golden:       #f4a261;
        --cream:        #fefae0;
        --text-dark:    #1a1a1a;
        --text-mid:     #4a4a4a;
        --white:        #ffffff;
    }

    /* Base */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Mukta', sans-serif;
        background-color: var(--cream);
    }

    /* Header */
    .kisan-header {
        background: linear-gradient(135deg, var(--green-dark) 0%, var(--green-mid) 60%, var(--green-light) 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 20px rgba(26,71,49,0.25);
    }
    .kisan-header-icon { font-size: 52px; }
    .kisan-header-title {
        font-family: 'Mukta', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: var(--white);
        line-height: 1.1;
        margin: 0;
    }
    .kisan-header-sub {
        font-size: 15px;
        color: var(--green-pale);
        margin: 4px 0 0 0;
    }

    /* Feature buttons */
    .feature-btn {
        background: var(--white);
        border: 2px solid var(--green-pale);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        height: 90px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .feature-btn:hover {
        border-color: var(--green-light);
        background: var(--green-pale);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(82,183,136,0.2);
    }
    .feature-btn-icon { font-size: 28px; }
    .feature-btn-label { font-size: 13px; font-weight: 600; color: var(--green-dark); margin-top: 4px; }

    /* Chat area */
    .chat-container {
        background: var(--white);
        border-radius: 16px;
        padding: 20px;
        min-height: 300px;
        border: 1.5px solid var(--green-pale);
        margin-bottom: 16px;
    }

    /* Message bubbles */
    .msg-user {
        background: var(--green-dark);
        color: var(--white);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 15px;
        line-height: 1.5;
    }
    .msg-bot {
        background: var(--green-pale);
        color: var(--text-dark);
        border-radius: 18px 18px 18px 4px;
        padding: 14px 18px;
        margin: 8px 0;
        max-width: 85%;
        font-size: 15px;
        line-height: 1.6;
        border-left: 3px solid var(--green-light);
    }
    .msg-label {
        font-size: 11px;
        font-weight: 600;
        opacity: 0.6;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Info cards */
    .info-card {
        background: var(--white);
        border-radius: 12px;
        padding: 16px;
        border: 1.5px solid var(--green-pale);
        margin-bottom: 12px;
    }
    .info-card-title {
        font-family: 'Mukta', sans-serif;
        font-weight: 700;
        font-size: 17px;
        color: var(--green-dark);
        margin-bottom: 8px;
    }

    /* Status indicator */
    .status-dot-green { color: #22c55e; }
    .status-dot-red { color: #ef4444; }

    /* Sidebar */
    .sidebar-title {
        font-family: 'Mukta', sans-serif;
        font-weight: 700;
        font-size: 20px;
        color: var(--green-dark);
        margin-bottom: 12px;
    }
    .tip-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-radius: 10px;
        padding: 14px;
        border-left: 4px solid var(--green-light);
        font-size: 13px;
        line-height: 1.6;
        color: var(--text-mid);
        margin-bottom: 10px;
    }

    /* Voice button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--green-mid), var(--green-dark));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Mukta', sans-serif;
        transition: all 0.2s;
        cursor: pointer;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--green-dark), #0f2d1e);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26,71,49,0.3);
    }

    /* Input box */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid var(--green-pale);
        font-family: 'Mukta', sans-serif;
        font-size: 15px;
        background: var(--white);
        padding: 12px 16px;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--green-light);
        box-shadow: 0 0 0 3px rgba(82,183,136,0.15);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid var(--green-pale);
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Loading spinner */
    .thinking-text {
        color: var(--green-mid);
        font-style: italic;
        font-size: 14px;
        padding: 8px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "region" not in st.session_state:
    st.session_state.region = "punjab"
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kisan-header">
    <div class="kisan-header-icon">🌾</div>
    <div>
        <p class="kisan-header-title">Kisan Mitra</p>
        <p class="kisan-header-sub">प्राकृतिक खेती सलाहकार · Natural Farming Consultant · Voice-Enabled</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚙️ Settings</p>', unsafe_allow_html=True)
    
    # TTS toggle
    st.session_state.tts_enabled = st.toggle(
        "🔊 Awaaz Enable Karein (TTS)",
        value=st.session_state.tts_enabled,
        help="Bot ki awaaz sunne ke liye ON karein"
    )
    
    # Region selector
    st.session_state.region = st.selectbox(
        "📍 Aapka Kshetra (Your Region)",
        options=["punjab", "haryana", "uttar_pradesh", "maharashtra", "rajasthan"],
        format_func=lambda x: {
            "punjab": "Punjab",
            "haryana": "Haryana",
            "uttar_pradesh": "Uttar Pradesh",
            "maharashtra": "Maharashtra",
            "rajasthan": "Rajasthan"
        }[x],
        index=0
    )
    
    st.divider()
    
    # Quick tips
    st.markdown('<p class="sidebar-title">💡 Quick Tips</p>', unsafe_allow_html=True)
    
    tips = [
        "🌿 **Jeevamrit** — Gaay ke gobar se bana jaivik khad, fasal ke liye amrit",
        "🐛 **Neem tel** — Keede maar dawa ka sabse accha vikalp",
        "🌱 **Intercropping** — Ek saath kai faslein ugana, zyada kamai",
        "💧 **Mulching** — Mitti mein naami banaye rakhta hai"
    ]
    
    for tip in tips:
        st.markdown(f'<div class="tip-box">{tip}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Chat Saaf Karein"):
        st.session_state.messages = []
        st.session_state.last_audio = None
        st.rerun()

# ─── Main Layout ────────────────────────────────────────────────────────────────
col_chat, col_info = st.columns([3, 2], gap="large")

with col_chat:
    st.markdown("### 💬 Kisan Mitra se Baat Karein")
    
    # ── Voice Input (Browser STT) ──────────────────────────────────────────────
    st.markdown("""
    <div style="background:#f0fdf4; border-radius:12px; padding:16px; margin-bottom:16px; border:1.5px solid #bbf7d0;">
        <p style="margin:0 0 8px 0; font-weight:600; color:#166534; font-size:15px;">🎤 Voice Input (Browser Microphone)</p>
        <p style="margin:0; color:#4a4a4a; font-size:13px;">Neeche mic button dabayein, apna sawaal bolein, phir Send karein</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Web Speech API via JS component
    voice_html = """
    <div style="margin-bottom:12px;">
        <button id="micBtn" onclick="startVoice()" style="
            background: linear-gradient(135deg, #2d6a4f, #1a4731);
            color: white; border: none; border-radius: 10px;
            padding: 12px 24px; font-size: 15px; font-weight: 600;
            cursor: pointer; width: 100%; transition: all 0.2s;
            display: flex; align-items: center; justify-content: center; gap: 8px;">
            🎤 Mic Dabayein — Sawaal Bolein
        </button>
        <div id="status" style="margin-top:8px; font-size:13px; color:#666; text-align:center;"></div>
        <input id="voiceText" type="text" placeholder="Yahan aapki awaaz text mein aayegi..."
            style="width:100%; margin-top:8px; padding:10px 14px; border:2px solid #bbf7d0;
            border-radius:8px; font-size:14px; font-family:inherit; box-sizing:border-box;"/>
        <button onclick="sendVoiceText()" style="
            background:#52b788; color:white; border:none; border-radius:8px;
            padding:8px 20px; margin-top:8px; font-size:14px; cursor:pointer; width:100%;">
            ✅ Is sawaal ko bhejein
        </button>
    </div>
    
    <script>
    let recognition;
    
    function startVoice() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            document.getElementById('status').innerHTML = '❌ Aapka browser voice support nahi karta. Chrome use karein.';
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'hi-IN';
        recognition.interimResults = true;
        recognition.continuous = false;
        
        document.getElementById('micBtn').innerHTML = '🔴 Sun raha hoon... (dobara dabayein rokne ke liye)';
        document.getElementById('micBtn').style.background = 'linear-gradient(135deg, #dc2626, #991b1b)';
        document.getElementById('status').innerHTML = '🎤 Bol rahe hain...';
        
        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            document.getElementById('voiceText').value = transcript;
        };
        
        recognition.onend = function() {
            document.getElementById('micBtn').innerHTML = '🎤 Mic Dabayein — Sawaal Bolein';
            document.getElementById('micBtn').style.background = 'linear-gradient(135deg, #2d6a4f, #1a4731)';
            document.getElementById('status').innerHTML = '✅ Awaaz capture ho gayi! "Is sawaal ko bhejein" press karein.';
        };
        
        recognition.onerror = function(event) {
            document.getElementById('status').innerHTML = '❌ Error: ' + event.error + '. Dobara try karein.';
            document.getElementById('micBtn').innerHTML = '🎤 Mic Dabayein — Sawaal Bolein';
            document.getElementById('micBtn').style.background = 'linear-gradient(135deg, #2d6a4f, #1a4731)';
        };
        
        recognition.start();
    }
    
    function sendVoiceText() {
        const text = document.getElementById('voiceText').value.trim();
        if (text) {
            // Send to Streamlit via URL param trick
            window.parent.postMessage({type: 'voice_input', text: text}, '*');
            document.getElementById('status').innerHTML = '📤 Bheja ja raha hai...';
        } else {
            document.getElementById('status').innerHTML = '⚠️ Pehle kuch bolein ya neeche type karein.';
        }
    }
    </script>
    """
    
    components.html(voice_html, height=220)
    
    # ── Text Input ─────────────────────────────────────────────────────────────
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "✍️ Ya Type Karein (Or type here)",
            placeholder="Jaise: Mere tamatar ke patte par safed daag aa rahe hain...",
            label_visibility="visible"
        )
        
        col_send, col_quick = st.columns([2, 3])
        with col_send:
            submitted = st.form_submit_button("📤 Bhejein (Send)", use_container_width=True)
    
    # ── Quick Question Buttons ──────────────────────────────────────────────────
    st.markdown("**⚡ Jaldi Poochein:**")
    qcol1, qcol2, qcol3 = st.columns(3)
    
    quick_q = None
    with qcol1:
        if st.button("🌦️ Mausam\nbatao", use_container_width=True, key="q1"):
            quick_q = f"Mera kshetra {st.session_state.region} hai. Aaj ka mausam kaisa hai aur khet ke liye kya salah hai?"
    with qcol2:
        if st.button("💰 Mandi\nbhav", use_container_width=True, key="q2"):
            quick_q = "Aaj ki mandi mein kaunsi fasal ki sabse achi kimat mil rahi hai? Market bhav batao."
    with qcol3:
        if st.button("🌿 Jeevamrit\nbanayen", use_container_width=True, key="q3"):
            quick_q = "Jeevamrit kaise banate hain? Puri recipe aur tarika batao."
    
    # Process input
    final_input = None
    if submitted and user_input.strip():
        final_input = user_input.strip()
    elif quick_q:
        final_input = quick_q
    
    if final_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": final_input})
        
        # Get AI response
        with st.spinner("🌾 Kisan Mitra soch raha hai..."):
            history = st.session_state.messages[:-1]  # exclude current
            response = get_ai_response(
                final_input,
                conversation_history=[{"role": m["role"], "content": m["content"]} for m in history]
            )
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Store response text for browser TTS
        if st.session_state.tts_enabled:
            st.session_state.last_audio = response

        st.rerun()
    
    # ── Chat History ───────────────────────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding:40px 20px; color:#666;">
            <div style="font-size:48px; margin-bottom:12px;">🌾</div>
            <p style="font-size:18px; font-weight:600; color:#2d6a4f;">Namaste Kisan Bhai!</p>
            <p style="font-size:15px;">Apna sawaal type karein ya mic dabayein.<br>
            Main aapki madad ke liye hoon — bimari, mausam, mandi bhav, kuch bhi poochein!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display messages (newest first or chronological)
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_html += f"""
                <div style="display:flex; justify-content:flex-end; margin:8px 0;">
                    <div class="msg-user">
                        <div class="msg-label">Aap 👤</div>
                        {msg["content"]}
                    </div>
                </div>"""
            else:
                chat_html += f"""
                <div style="display:flex; justify-content:flex-start; margin:8px 0;">
                    <div class="msg-bot">
                        <div class="msg-label">🌾 Kisan Mitra</div>
                        {msg["content"]}
                    </div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    
    # Play TTS via browser Web Speech API
    if st.session_state.last_audio and st.session_state.tts_enabled:
        tts_html = get_browser_tts_html(st.session_state.last_audio)
        components.html(tts_html, height=0)
        st.session_state.last_audio = None


# ─── Info Panel ─────────────────────────────────────────────────────────────────
with col_info:
    # Weather card
    st.markdown("### 🌤️ Mausam Jaankari")
    weather_summary = get_weather_summary(st.session_state.region)
    st.markdown(f"""
    <div class="info-card">
        {weather_summary.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    # Market prices
    st.markdown("### 📊 Mandi Bhav")
    market_summary = get_market_summary()
    st.markdown(f"""
    <div class="info-card" style="max-height:280px; overflow-y:auto;">
        {market_summary.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    # Quick disease reference
    st.markdown("### 🔬 Jaldi Pehchan")
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">Aam Bimariyan</div>
        <table style="width:100%; font-size:13px; border-collapse:collapse;">
            <tr style="background:#f0fdf4;">
                <th style="padding:6px; text-align:left; border-bottom:1px solid #bbf7d0;">Lakshan</th>
                <th style="padding:6px; text-align:left; border-bottom:1px solid #bbf7d0;">Bimari</th>
            </tr>
            <tr><td style="padding:5px;">Safed daag</td><td style="padding:5px;">Powdery Mildew</td></tr>
            <tr style="background:#f9fafb;"><td style="padding:5px;">Bhoora/Peela daag</td><td style="padding:5px;">Jhulsa Rog (Blast)</td></tr>
            <tr><td style="padding:5px;">Paudha murjhana</td><td style="padding:5px;">Jadon ka sarana</td></tr>
            <tr style="background:#f9fafb;"><td style="padding:5px;">Chote keede</td><td style="padding:5px;">Maahu (Aphids)</td></tr>
            <tr><td style="padding:5px;">Patte mein chhed</td><td style="padding:5px;">Patton ka Keeda</td></tr>
        </table>
        <p style="font-size:12px; color:#666; margin:8px 0 0 0;">💬 Kisan Mitra se poochhen: "Mere [fasal] ke patte par [lakshan] hain"</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px; color:#888; font-size:12px; margin-top:24px; border-top:1px solid #e0e0e0;">
    🌾 Kisan Mitra — Connecting Dreams Foundation · CDF Round 2 Project<br>
    Voice-Based Natural Farming Consultant · Built with Claude AI + Streamlit<br>
    <em>Jaivik Kheti ko badhawa dene ke liye bana hai — For Natural Farming Promotion</em>
</div>
""", unsafe_allow_html=True)
