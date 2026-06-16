# Nova — Rule-Based AI Chatbot
---

## Project Description

**Nova** is a rule-based AI chatbot web application built entirely with Python. It demonstrates fundamental AI concepts — decision-making, control flow, and rule-based response generation — without using any machine learning models or external APIs.

The project is split into two clean layers:
- **`chatbot.py`** — the brain (logic, rules, matching engine)
- **`app.py`** — the face (Streamlit UI, session management, display)

---

## Objective

- Understand and implement rule-based AI systems
- Practice clean code architecture with separation of concerns
- Build a deployable web application using Streamlit
- Demonstrate NLP-adjacent concepts like keyword matching and input normalization

---

## Features

| Feature | Details |
|---|---|
|  Greeting Handling | hello, hi, hey, good morning, good evening |
|  FAQ Responses | name, creator, age, capabilities, how are you |
|  Live Time & Date | Returns the actual current time/date |
|  Joke Generator | 4 rotating programming jokes |
|  Partial Matching | "tell me your name" matches "your name" |
|  Case-Insensitive | Input is normalized before matching |
|  Random Responses | Multiple replies per rule for variety |
|  Chat History | Full session history via `st.session_state` |
|  Quick Suggestions | Sidebar buttons to try example prompts |
|  Clear Chat | Reset the entire conversation |
|  Exit Commands | bye / goodbye / quit / exit / farewell |
|  Session Stats | Live message count in the sidebar |

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core programming language |
| **Streamlit** | Web UI framework |
| `random` | Random response selection |
| `datetime` | Live time and date responses |

**No machine learning. No external APIs. No databases.**

---

## Project Structure

```
Project-1-Rule-Based-Chatbot/
│
├── app.py              # Streamlit UI — page layout, input handling, chat display
├── chatbot.py          # Chatbot logic — rules, matching engine, response selection
├── requirements.txt    # Python dependencies (just Streamlit!)
├── README.md           # This file
└── screenshots/        # App screenshots for portfolio
```

---

## How the Chatbot Works

```
User Input: "Hey! What's YOUR name?"
                │
                ▼
        1. Normalize Input
           → "hey! what's your name?"
                │
                ▼
        2. Loop Through RULES list
           → Check each rule's keywords
           → "your name" found in input 
                │
                ▼
        3. Pick random response
           → "I'm Nova 🤖 — a rule-based AI chatbot!"
                │
                ▼
        4. Resolve special tokens
           → No @TIME or @DATE token, return as-is
                │
                ▼
        5. Display in UI
```

### Matching Strategy: Partial Keyword Matching

Instead of requiring exact input, the engine checks if any keyword **appears anywhere in** the normalized input string:

```python
if keyword in normalized_input:   # "your name" in "tell me your name" → True 
```

This makes the bot much more natural to interact with.

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone or download the project
git clone https://github.com/yourusername/Project-1-Rule-Based-Chatbot.git
cd Project-1-Rule-Based-Chatbot

# 2. (Recommended) Create a virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`.

---

## Screenshots

| Chat Interface | Sidebar |
|---|---|
| ![Chat](screenshots/chat.png) | ![Sidebar](screenshots/sidebar.png) |

---

## 💬 Example Conversations

```
You:   Hello!
Nova:  Hey there! 👋 I'm Nova. How can I help you today?

You:   What can you do?
Nova:  💬 Chat & Answer Questions...
       🧠 Rule-Based Responses...
       🕐 Tell you the time/date...

You:   Tell me a joke
Nova:  Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂

You:   What time is it?
Nova:  The current time is ⏰ 02:30 PM.

You:   bye
Nova:  Goodbye! 👋 It was great chatting with you. Come back anytime!
```

---

## 🚀 Possible Improvements (Next Steps)

1. **Add more topics** — weather responses, math calculations, trivia
2. **Sentiment detection** — detect positive/negative mood and adjust tone
3. **User name memory** — ask the user's name and use it in replies
4. **Export chat** — download conversation as a .txt or .pdf file
5. **Text-to-speech** — read responses aloud using `pyttsx3`
6. **Deploy to cloud** — host free on Streamlit Community Cloud
7. **Multi-language** — detect and reply in the user's language

---

## 👨‍💻 Author

Built as an internship project to demonstrate rule-based AI and Python web development.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
