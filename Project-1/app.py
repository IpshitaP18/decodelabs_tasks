import streamlit as st
import time
from chatbot import (
    get_response,
    is_exit_command,
    get_welcome_message,
    resolve_special_tokens,
    CHATBOT_NAME
)

st.set_page_config(
    page_title=f"{CHATBOT_NAME} — Vibrant AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 50%, #e0f2fe 100%);
        color: #1e293b;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
    }

    .chat-header h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff7e5f, #feb47b, #2563eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-align: center;
    }
    
    .chat-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-top: -5px;
        margin-bottom: 25px;
    }

    .status-online {
        display: inline-block;
        background: #0ea5e9;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px rgba(14, 165, 233, 0.6);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%   { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.4); }
        70%  { transform: scale(1); box-shadow: 0 0 0 8px rgba(14, 165, 233, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }
    }

    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stChatMessage"]:has(div[data-testid="stMarkdownContainer"] p:contains("You")) {
        border-left: 5px solid #ff7e5f !important;
    }
    
    [data-testid="stChatMessage"]:has(img) {
        border-left: 5px solid #2563eb !important;
    }

    .stButton button {
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.8) !important;
        color: #334155 !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%) !important;
        color: white !important;
        border: none !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(254, 180, 123, 0.4) !important;
    }

    div[data-testid="stMetricValue"] {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "avatar": "🤖", "content": get_welcome_message()}
    ]

if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

with st.sidebar:
    st.markdown(f"## 🤖 About {CHATBOT_NAME}")
    st.markdown("""
    A bright, rule-based AI companion crafted with pure Python logic.
    
    - **Engine:** Keyword Matching
    - **Framework:** Streamlit UI
    - **Palette:** Light & Dynamic
    """)

    st.divider()

    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Input", f"{st.session_state.message_count} 💬")
    with col2:
        total_bot = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        st.metric("Nova Reply", f"{total_bot} ⚡")

    st.divider()

    st.markdown("### 💡 Quick Prompts")
    suggestions = [
        "What can you do?",
        "Tell me a joke",
        "What time is it?",
        "What is AI?",
    ]
    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True, key=f"sug_{suggestion}"):
            if not st.session_state.conversation_ended:
                st.session_state.pending_input = suggestion
                st.rerun()

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "avatar": "🤖", "content": get_welcome_message()}
        ]
        st.session_state.conversation_ended = False
        st.session_state.message_count = 0
        st.rerun()


st.markdown(f'<div class="chat-header"><h1>{CHATBOT_NAME} Assistant</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle"><span class="status-online"></span>Systems Active · Core Version 2.0</div>', unsafe_allow_html=True)

for message in st.session_state.messages:
    avatar = message.get("avatar", "👤")
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if "pending_input" in st.session_state and not st.session_state.conversation_ended:
    user_input = st.session_state.pop("pending_input")
else:
    user_input = None

if st.session_state.conversation_ended:
    st.warning("🔒 Session concluded. Use 'Clear Conversation' in the sidebar to start fresh.")
else:
    prompt = st.chat_input("Message Nova...")
    
    if user_input:
        prompt = user_input

    if prompt:
        user_msg = prompt.strip()

        st.session_state.messages.append({"role": "user", "avatar": "👤", "content": user_msg})
        st.session_state.message_count += 1
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_msg)

        bot_reply = get_response(user_msg)
        bot_reply = resolve_special_tokens(bot_reply)

        with st.spinner("Thinking..."):
            time.sleep(0.35)

        st.session_state.messages.append({"role": "assistant", "avatar": "🤖", "content": bot_reply})

        if is_exit_command(user_msg):
            st.session_state.conversation_ended = True

        st.rerun()

st.markdown("""
<div style='text-align:center; color:#94a3b8; font-size:11px; margin-top:30px; letter-spacing: 0.5px;'>
    Tip: Type <span style="color:#ff7e5f; font-weight:bold;">"bye"</span> to end the chat · <span style="color:#2563eb; font-weight:bold;">"what can you do"</span> for features.
</div>
""", unsafe_allow_html=True)
