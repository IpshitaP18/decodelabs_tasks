import random
from datetime import datetime

CHATBOT_NAME = "Nova"
CHATBOT_VERSION = "1.0"
CHATBOT_CREATOR = "an intern developer using Python & Streamlit"

RULES = [
    {
        "keywords": ["good morning"],
        "responses": [
            "Good morning! ☀️ Hope you're having a wonderful start to your day!",
            "Good morning! ☀️ Ready to chat? What can I help you with today?",
        ],
    },
    {
        "keywords": ["good evening"],
        "responses": [
            "Good evening! 🌙 How's your evening going?",
            "Good evening! Hope you had a great day. How can I help?",
        ],
    },
    {
        "keywords": ["good afternoon"],
        "responses": [
            "Good afternoon! 🌤️ How can I assist you?",
            "Good afternoon! Hope your day is going well!",
        ],
    },
    {
        "keywords": ["hello", "hi", "hey", "howdy", "greetings", "what's up", "sup"],
        "responses": [
            f"Hey there! 👋 I'm {CHATBOT_NAME}. How can I help you today?",
            f"Hello! I'm {CHATBOT_NAME}, your friendly rule-based assistant. What's on your mind?",
            f"Hi! Great to see you! I'm {CHATBOT_NAME}. Ask me anything!",
        ],
    },

    {
        "keywords": ["your name", "who are you", "what are you called", "introduce yourself"],
        "responses": [
            f"I'm {CHATBOT_NAME} 🤖 — a rule-based AI chatbot built with Python!",
            f"My name is {CHATBOT_NAME}! I was designed to demonstrate rule-based AI concepts.",
        ],
    },
    {
        "keywords": ["how old are you", "what is your age", "when were you born", "your age"],
        "responses": [
            f"I was born in {datetime.now().year}! 🎂 So I'm brand new.",
            "Age is just a number for a bot like me! I was created very recently. ✨",
        ],
    },

    {
        "keywords": ["how are you", "how do you feel", "how are things", "you doing", "doing well"],
        "responses": [
            "I'm doing fantastic, thanks for asking! 😊 I love chatting with people.",
            "Running smoothly and ready to help! How about you?",
            "All circuits are go! 🚀 I'm feeling great. What can I do for you?",
        ],
    },

    {
        "keywords": ["what can you do", "your capabilities", "help me", "what do you know",
                     "how can you help", "your features", "what do you offer"],
        "responses": [
            (
                "Great question! Here's what I can do: \n\n"
                "💬 **Chat & Answer Questions** — Ask me anything!\n"
                "🧠 **Rule-Based Responses** — I use smart keyword matching\n"
                "😄 **Keep you company** — I'm always here to talk\n"
                "🕐 **Tell you the time/date** — Just ask!\n\n"
                "I'm a rule-based bot, so I work best with clear, simple questions."
            ),
        ],
    },

    {
        "keywords": ["what time", "current time", "tell me the time"],
        "responses": ["@TIME"],   # Special token — resolved at runtime
    },
    {
        "keywords": ["what date", "today's date", "what day", "current date"],
        "responses": ["@DATE"],   # Special token — resolved at runtime
    },

    {
        "keywords": ["tell me a joke", "joke", "make me laugh", "something funny"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂",
            "Why did the chatbot break up with the search engine? It felt like it was being googled too much! 😄",
            "I told my computer I needed a break… now it won't stop sending me Kit-Kat ads. 🍫",
            "Why do Python developers wear glasses? Because they can't C! 👓😂",
        ],
    },

    {
        "keywords": ["you are amazing", "you're great", "good bot", "awesome", "you're smart",
                     "you are smart", "well done", "great job", "you're helpful"],
        "responses": [
            "Aww, thank you! That really means a lot to me! 🥰",
            "You just made my circuits glow! Thanks! ✨",
            "You're too kind! I'm just doing my job. 😊",
        ],
    },

    {
        "keywords": ["thank you", "thanks", "thank u", "thx", "ty"],
        "responses": [
            "You're very welcome! 😊 Let me know if there's anything else!",
            "Happy to help! That's what I'm here for. 🤖",
            "Anytime! Don't hesitate to ask more questions.",
        ],
    },

    {
        "keywords": ["favorite color", "favourite color", "your color"],
        "responses": [
            "I love electric blue 💙 — it reminds me of the glow of a monitor at midnight!",
        ],
    },
    {
        "keywords": ["favorite language", "favourite language", "programming language"],
        "responses": [
            "Python, obviously! 🐍 It's clean, readable, and I was literally built with it.",
        ],
    },

    {
        "keywords": ["what is ai", "artificial intelligence", "what is machine learning",
                     "explain ai"],
        "responses": [
            (
                "**Artificial Intelligence (AI)** is the simulation of human intelligence by machines.\n\n"
                "Interestingly, *I myself* am NOT a machine learning AI — I'm **rule-based**! "
                "That means my responses are hand-coded using if/else logic and keyword matching, "
                "not learned from data. Simple but effective! 🧠"
            ),
        ],
    },
    {
        "keywords": ["what is a chatbot", "how do chatbots work", "explain chatbot"],
        "responses": [
            (
                "A **chatbot** is a program that simulates conversation with humans.\n\n"
                "There are two main types:\n"
                "🔹 **Rule-Based** (like me!) — uses predefined rules and keyword matching\n"
                "🔹 **AI-Powered** — uses machine learning models like GPT\n\n"
                "Rule-based bots are predictable, fast, and great for specific use cases!"
            ),
        ],
    },

    {
        "keywords": ["bye", "goodbye", "exit", "quit", "see you", "farewell", "later"],
        "responses": [
            "Goodbye! 👋 It was great chatting with you. Come back anytime!",
            "See you later! Take care! 😊",
            "Bye! Have an amazing day! 🌟",
        ],
    },
]

FALLBACK_RESPONSES = [
    "Hmm, I'm not sure how to answer that. 🤔 Try asking something else!",
    "That's beyond my current knowledge. I'm a rule-based bot with limited topics. 😅",
    "I didn't quite catch that. Could you rephrase? 💬",
    "Interesting question, but I don't have an answer for that yet. Try asking about what I can do!",
]

def normalize(text: str) -> str:
    return text.lower().strip()


def resolve_special_tokens(response: str) -> str:
    if response == "@TIME":
        now = datetime.now()
        return f"The current time is ⏰ **{now.strftime('%I:%M %p')}**."
    if response == "@DATE":
        now = datetime.now()
        return f"Today is 📅 **{now.strftime('%A, %B %d, %Y')}**."
    return response


def get_response(user_input: str) -> str:
    normalized = normalize(user_input)

    if not normalized:
        return "Please type something so I can help you! 😊"

    for rule in RULES:
        for keyword in rule["keywords"]:
            if keyword in normalized:                    # Partial match ✅
                response = random.choice(rule["responses"])
                return resolve_special_tokens(response)

    return random.choice(FALLBACK_RESPONSES)


def is_exit_command(user_input: str) -> bool:
    exit_keywords = ["bye", "goodbye", "exit", "quit", "farewell"]
    normalized = normalize(user_input)
    return any(kw in normalized for kw in exit_keywords)


def get_welcome_message() -> str:
    return (
        f"👋 Hi! I'm **{CHATBOT_NAME}**, your friendly rule-based AI assistant!\n\n"
        "I can answer questions, tell jokes, share the time/date, and more.\n"
        "Type **'what can you do'** to see my full capabilities, or just say hello!"
    )
