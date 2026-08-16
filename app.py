import streamlit as st
from chatbot import ChatBot


# Cache the ChatBot instance so the model is trained only once per server lifecycle
@st.cache_resource
def load_bot(path: str = "intents.json"):
    return ChatBot(path)

# Load chatbot (cached)
bot = load_bot()
from datetime import datetime

# Load chatbot
bot = ChatBot("intents.json")

# Streamlit UI
st.set_page_config(page_title="College Chatbot", page_icon="🤖", layout="centered")

# App header
st.markdown(
    """
    <div style='display:flex;align-items:center;gap:12px'>
      <div style='font-size:36px'>🤖</div>
      <div>
        <h1 style='margin:0 0 4px 0'>College Assistant</h1>
        <div style='color: #9aa0a6;'>Ask about courses, admissions, timings and more.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Global styles for a professional dark chat look
st.markdown(
    """
    <style>
      :root { --bg:#0b0b0c; --card:#0f1720; --muted:#9aa0a6; --accent:#4f46e5; }
      html, body, [data-testid="stAppViewContainer"], [data-testid="stAppMain"], .stApp {
        background: var(--bg) !important;
        color: #e6eef8 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
      }
      .app-container { max-width: 900px; margin: 18px auto; }
      .chat-box { background: transparent; padding-top: 12px; }
      .bot-bubble, .user-bubble {
        display: inline-block; padding: 12px 16px; border-radius: 16px; max-width:70%; box-shadow: 0 2px 8px rgba(2,6,23,0.6);
        margin:8px 0; line-height:1.4;
      }
      .bot-bubble { background: #0f1720; color: #e6eef8; border: 1px solid rgba(255,255,255,0.03); }
      .user-bubble { background: linear-gradient(90deg,#2b3440,#1f2a36); color: #fff; float: right; text-align: right; }
      .meta { font-size:12px; color: var(--muted); margin-top:6px; }
      .input-row { display:flex; gap:8px; align-items:center; margin-top:12px; }
      .stTextInput>div>div>input { background:#0f1720 !important; color:#e6eef8 !important; border-radius:8px; }
      .stButton>button { background: var(--accent) !important; color: #fff !important; border-radius:8px; }
      .clear-btn { background: transparent; border: 1px solid rgba(255,255,255,0.06); color: var(--muted); padding:6px 10px; border-radius:8px }
      .welcome { color: var(--muted); margin-bottom:6px; }
      /* clear floats */
      .clearfix::after { content: ""; clear: both; display: table; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize chat history with a professional welcome message
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.history.append(("bot", "Hello! I'm the College Assistant — how can I help you today?"))

def timestamp():
    return datetime.now().strftime("%I:%M %p")

def send_message(user_text: str):
    if not user_text or not user_text.strip():
        return
    st.session_state.history.append(("user", user_text.strip(), timestamp()))
    # Show spinner while the bot generates a reply
    with st.spinner("Thinking..."):
        bot_reply = bot.get_response(user_text.strip())
    st.session_state.history.append(("bot", bot_reply, timestamp()))

def clear_chat():
    st.session_state.history = [("bot", "Hello! I'm the College Assistant — how can I help you today?", timestamp())]

container = st.container()
with container:
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)

    # Chat area
    st.markdown("<div class='chat-box clearfix'>", unsafe_allow_html=True)
    for item in st.session_state.history:
        # support old tuples without timestamp
        if len(item) == 2:
            sender, text = item
            time = ''
        else:
            sender, text, time = item

        if sender == "bot":
            st.markdown(
                f"<div style='display:flex;align-items:flex-start;gap:12px;margin-bottom:8px'>"
                f"<div style='width:40px;height:40px;border-radius:50%;background:#111827;display:flex;align-items:center;justify-content:center'>🤖</div>"
                f"<div><div class='bot-bubble'>{text}</div><div class='meta'>{time}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='display:flex;align-items:flex-start;gap:12px;justify-content:flex-end;margin-bottom:8px'>"
                f"<div><div class='user-bubble'>{text}</div><div class='meta'>{time}</div></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Input and controls
    col1, col2 = st.columns([8,1])
    with col1:
        with st.form(key="chat_form", clear_on_submit=True):
            # Provide a non-empty label for accessibility and hide it visually
            user_input = st.text_input("Your question", placeholder="Type your question here and press Send...", key="input", label_visibility="collapsed")
            submit = st.form_submit_button("Send")
            if submit:
                send_message(user_input)
    with col2:
        if st.button("Clear", key="clear"):
            clear_chat()

    st.markdown("</div>", unsafe_allow_html=True)

