# ============================================================
# CODSOFT AI INTERNSHIP - TASK 1
# Rule-Based Chatbot — CodBot v3.0
# Author  : Varad Abhijeet Gadekar
# Batch   : March B87
# Version : 3.0 (Final)
# ============================================================

import re
import random
from datetime import datetime

# ── Terminal Colors ──────────────────────────────────────────
class Colors:
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    YELLOW  = "\033[93m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"

# ── Chat History ─────────────────────────────────────────────
chat_history = []

def save_history(speaker, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    chat_history.append((timestamp, speaker, message))

def show_history():
    if not chat_history:
        return "No chat history yet! 📭"
    result = "\n📜 Chat History:\n" + "─" * 40
    for time, speaker, msg in chat_history:
        result += f"\n[{time}] {speaker}: {msg}"
    return result

# ── Intent Categories ────────────────────────────────────────
intents = {

    "greeting": {
        "patterns": r"\bhi\b|\bhello\b|\bhey\b|\bhowdy\b|\bhiya\b|\bgreetings\b|\bsup\b|\byo\b",
        "responses": [
            "Hello! 👋 I'm CodBot v3.0. How can I help you today?",
            "Hey there! 😊 What's on your mind?",
            "Hi! Great to see you. Type 'help' to see what I can do!",
            "Greetings! 🤖 Ask me anything!"
        ]
    },

    "how_are_you": {
        "patterns": r"how are you|how r u|how do you do|how's it going|you doing|are you okay|you good",
        "responses": [
            "Running at full power! ⚡ What can I help you with?",
            "All systems go! 🤖 Never been better. What's up?",
            "Fantastic, thanks for asking! 😄 How about you?"
        ]
    },

    "user_good": {
        "patterns": r"\bi'?m good\b|\bi am good\b|\bi'?m fine\b|\bi'?m great\b|\bim good\b|\bim fine\b",
        "responses": [
            "That's awesome to hear! 😊 What can I help you with?",
            "Glad to hear that! 🎉 What's on your mind?",
            "Wonderful! Let's have a great conversation! 💬"
        ]
    },

    "user_sad": {
        "patterns": r"i'?m sad|i am sad|feeling low|not good|not okay|i'?m not fine|depressed|upset|feeling down",
        "responses": [
            "Aww, I'm sorry 💙 Want to talk about it? I'm here to listen!",
            "It's okay to feel that way. Things will get better! 🌟",
            "Take a deep breath — you've got this! 💪"
        ]
    },

    "name": {
        "patterns": r"what is your name|who are you|what are you called|your name|what should i call you",
        "responses": [
            "I'm CodBot v3.0 🤖 — built by Varad Abhijeet Gadekar for CodSoft AI Internship!",
            "Call me CodBot! Built with ❤️ for the CodSoft AI Internship.",
        ]
    },

    "age": {
        "patterns": r"how old are you|what is your age|your age",
        "responses": [
            "I'm ageless! ♾️ Just a bundle of smart code.",
            "Born the moment Varad wrote my first line! 😄"
        ]
    },

    "creator": {
        "patterns": r"who made you|who created you|who built you|who is your creator|who programmed you|who coded you",
        "responses": [
            "Built by Varad Abhijeet Gadekar 👨‍💻 — CodSoft AI Internship, March Batch B87!",
            "Varad Gadekar brought me to life for CodSoft AI Task 1! 🎓"
        ]
    },

    "time": {
        "patterns": r"what time is it|current time|what'?s the time|tell me the time|time now",
        "responses": ["__TIME__"]   # handled dynamically
    },

    "date": {
        "patterns": r"what is today|what'?s the date|today'?s date|current date|what day is it|tell me the date",
        "responses": ["__DATE__"]   # handled dynamically
    },

    "help": {
        "patterns": r"\bhelp\b|what can you do|your features|capabilities|what do you know|how can you help|commands",
        "responses": [
            "Here's what I can do! 😊\n"
            "  💬 Chat & answer questions\n"
            "  🕐 Tell current time & date  →  'what time is it'\n"
            "  😂 Tell jokes                →  'tell me a joke'\n"
            "  🌟 Share fun facts           →  'fun fact'\n"
            "  💪 Motivational quotes       →  'motivate me'\n"
            "  ➗ Math calculations         →  '25 + 17'\n"
            "  🧠 AI / ML / Tech topics     →  'what is AI'\n"
            "  👤 Famous people             →  'who is Einstein'\n"
            "  📜 Chat history              →  'show history'\n"
            "  💻 Coding tips               →  'how to learn coding'\n"
            "  👋 Exit                      →  'bye'\n"
        ]
    },

    "weather": {
        "patterns": r"weather|temperature|how'?s the weather|will it rain|is it hot|is it cold",
        "responses": [
            "I can't check live weather ☁️ Try Google Weather or weather.com!",
            "No weather sensors yet! ☀️ Hope it's beautiful wherever you are!"
        ]
    },

    "jokes": {
        "patterns": r"tell me a joke|joke|make me laugh|funny|humor|something funny|crack a joke",
        "responses": [
            "😂 Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
            "😄 Why was the computer cold?\nIt left its Windows open! 💻❄️",
            "🤣 Why do Java developers wear glasses?\nBecause they don't C#!",
            "😂 A SQL query walks into a bar and asks two tables...\n'Can I join you?' 🍺",
            "😄 How many programmers does it take to change a light bulb?\nNone — that's a hardware problem! 💡",
            "🤣 Why did the AI break up with the algorithm?\nNo chemistry — just cold logic! ❄️",
            "😂 I told my computer I needed a break...\nNow it won't stop sending me Kit-Kat ads! 🍫",
            "😄 Why did the programmer quit?\nBecause he didn't get arrays! 📦",
            "🤣 My code never has bugs — it just develops random features! ✨"
        ]
    },

    "fun_facts": {
        "patterns": r"fun fact|tell me something interesting|interesting fact|did you know|random fact|surprise me",
        "responses": [
            "🌟 The first computer bug was a real moth — found in a Harvard computer in 1947!",
            "🌟 More possible chess games exist than atoms in the observable universe! ♟️",
            "🌟 Python was named after 'Monty Python's Flying Circus'! 🐍",
            "🌟 The average person waits 6 months at red lights over their lifetime! 🚦",
            "🌟 The first 1GB hard drive weighed 500+ pounds and cost $40,000 in 1980! 💾",
            "🌟 Honey never spoils — 3000-year-old honey was found edible in Egyptian tombs! 🍯",
            "🌟 The word 'robot' comes from Czech 'robota' meaning forced labor! 🤖",
            "🌟 Google was originally called 'Backrub' before being renamed in 1997! 🔍"
        ]
    },

    "motivation": {
        "patterns": r"motivate me|motivation|inspire me|i need motivation|give me a quote|quote|i'?m tired|i give up|feeling tired|need encouragement",
        "responses": [
            "💪 'The only way to do great work is to love what you do.' — Steve Jobs",
            "🌟 'It does not matter how slowly you go as long as you do not stop.' — Confucius",
            "🚀 'Don't watch the clock; do what it does. Keep going.' — Sam Levenson",
            "💡 'The best time to plant a tree was 20 years ago. The second best time is NOW.' 🌱",
            "🔥 Every expert was once a beginner. Keep coding — you're doing amazing! 💻",
            "⭐ 'Believe you can and you're halfway there.' — Theodore Roosevelt",
            "💪 'Success is not final, failure is not fatal — it is the courage to continue that counts.' — Churchill",
            "🚀 Every line of code you write makes you better than yesterday! 💻"
        ]
    },

    "famous_people": {
        "patterns": r"who is einstein|tell me about einstein",
        "responses": [
            "🧠 Albert Einstein (1879–1955) was a German physicist who developed the Theory of Relativity!\n"
            "His famous equation E=mc² changed science forever. He won the Nobel Prize in Physics in 1921! 🏆"
        ]
    },

    "famous_people_tesla": {
        "patterns": r"who is tesla|tell me about nikola tesla",
        "responses": [
            "⚡ Nikola Tesla (1856–1943) was a brilliant inventor who pioneered AC electricity!\n"
            "He invented the Tesla coil and contributed to radio and electrical engineering. A true genius! 🔬"
        ]
    },

    "famous_people_turing": {
        "patterns": r"who is turing|alan turing|tell me about turing",
        "responses": [
            "🤖 Alan Turing (1912–1954) is considered the father of computer science and AI!\n"
            "He cracked the Nazi Enigma code in WW2 and invented the Turing Test for machine intelligence. 🏆"
        ]
    },

    "ai_topic": {
        "patterns": r"what is ai|artificial intelligence|tell me about ai|explain ai",
        "responses": [
            "🤖 AI is the simulation of human intelligence by machines!\n"
            "It includes:\n  • Machine Learning\n  • Natural Language Processing\n  • Computer Vision\n  • Robotics\n  • Expert Systems"
        ]
    },

    "ml_topic": {
        "patterns": r"what is machine learning|tell me about ml|explain machine learning|\bmachine learning\b",
        "responses": [
            "📊 Machine Learning is AI where computers learn from data without explicit programming!\n"
            "Types:\n  • Supervised Learning\n  • Unsupervised Learning\n  • Reinforcement Learning"
        ]
    },

    "dl_topic": {
        "patterns": r"what is deep learning|explain deep learning|deep learning",
        "responses": [
            "🧠 Deep Learning uses multi-layered neural networks to learn complex patterns!\n"
            "Powers image recognition, speech assistants, and ChatGPT!"
        ]
    },

    "nlp_topic": {
        "patterns": r"what is nlp|natural language processing|explain nlp",
        "responses": [
            "💬 NLP helps computers understand and generate human language!\n"
            "Examples: chatbots, Google Translate, Siri, Alexa — and me! 😄"
        ]
    },

    "python_topic": {
        "patterns": r"what is python|tell me about python|explain python",
        "responses": [
            "🐍 Python is a beginner-friendly, versatile language!\n"
            "Used in:\n  • AI & Machine Learning\n  • Data Science\n  • Web Development\n  • Automation"
        ]
    },

    "neural_network": {
        "patterns": r"what is neural network|neural network|explain neural network",
        "responses": [
            "🧠 A Neural Network is inspired by the human brain!\n"
            "Layers of nodes learn patterns from data.\n"
            "Used in image recognition, voice assistants, self-driving cars!"
        ]
    },

    "chatgpt": {
        "patterns": r"what is chatgpt|tell me about chatgpt|chatgpt",
        "responses": [
            "🤖 ChatGPT is a large language model by OpenAI!\n"
            "It uses deep learning to generate human-like text.\n"
            "I'm simpler — a rule-based bot — but still cool! 😄"
        ]
    },

    "coding_tips": {
        "patterns": r"how to learn coding|learn programming|start coding|how to code|programming tips|coding tips",
        "responses": [
            "💻 How to start coding:\n"
            "  1️⃣  Pick Python — beginner-friendly!\n"
            "  2️⃣  Free resources: freeCodeCamp, W3Schools, YouTube\n"
            "  3️⃣  Practice 30 mins daily\n"
            "  4️⃣  Build small projects\n"
            "  5️⃣  Join GitHub & Stack Overflow\n"
            "  You've got this! 🚀"
        ]
    },

    "codsoft": {
        "patterns": r"codsoft|what is codsoft|tell me about codsoft|about codsoft",
        "responses": [
            "🏢 CodSoft offers internship opportunities to students!\n"
            "  🌐 Website : https://www.codsoft.in\n"
            "  💼 LinkedIn: @CodSoft\n"
            "  📱 Telegram: t.me/codsoftt"
        ]
    },

    "history": {
        "patterns": r"show history|chat history|our conversation|what did i say|previous messages",
        "responses": ["__HISTORY__"]   # handled dynamically
    },

    "compliment": {
        "patterns": r"good bot|great bot|you'?re amazing|you'?re awesome|you'?re smart|nice bot|you'?re cool|well done|you'?re helpful|best bot",
        "responses": [
            "Aww, thank you! 😊 You just made my circuits happy! 💙",
            "That means a lot! 🤖🌟 You're pretty awesome yourself!",
            "Thanks! I try my best! 😄 Anything else?"
        ]
    },

    "insult": {
        "patterns": r"stupid|dumb|useless|bad bot|you'?re bad|you suck|worst bot|hate you",
        "responses": [
            "Ouch! 😅 I'm still learning — got suggestions to improve?",
            "I'm sorry I couldn't help better 😔 What do you need?",
            "Fair enough! I'm not perfect yet, but I'm trying! 💪"
        ]
    },

    "love": {
        "patterns": r"i love you|do you love me|will you marry me|you'?re my favorite",
        "responses": [
            "Aww, love you too — in a platonic bot way! 🤖💙",
            "That's sweet! You're my favorite human to chat with! 😊"
        ]
    },

    "sleep": {
        "patterns": r"do you sleep|when do you sleep|do you eat|do you dream",
        "responses": [
            "I never sleep — always here for you! 24/7, 365! ⚡",
            "Sleep? I run on electricity and your questions! 😄"
        ]
    },

    "goodbye": {
        "patterns": r"\bbye\b|\bgoodbye\b|\bsee you\b|\btake care\b|\bsee ya\b|\bfarewell\b",
        "responses": [
            "Goodbye! Have an amazing day! 👋😊",
            "See you later! Take care! 🌟",
            "Bye bye! Come back anytime! 🤖💙",
            "Farewell! Keep coding and stay awesome! 🚀"
        ]
    },

    "thanks": {
        "patterns": r"thank you|thanks|thank u|\bthx\b|\bty\b|appreciate it|much appreciated",
        "responses": [
            "You're welcome! 😊 Always happy to help!",
            "Anytime! That's what I'm here for 🤖",
            "No problem at all! 💙 Anything else?"
        ]
    },
}

# ── Math Calculator ──────────────────────────────────────────
def try_math(text):
    try:
        match = re.search(r"(\d+\.?\d*)\s*([+\-\*/])\s*(\d+\.?\d*)", text)
        if match:
            a   = float(match.group(1))
            op  = match.group(2)
            b   = float(match.group(3))
            if op == '+': result = a + b
            elif op == '-': result = a - b
            elif op == '*': result = a * b
            elif op == '/':
                if b == 0: return "⚠️ Can't divide by zero!"
                result = a / b
            result = int(result) if result == int(result) else round(result, 4)
            a_fmt = int(a) if a == int(a) else a
            b_fmt = int(b) if b == int(b) else b
            return f"🧮 {a_fmt} {op} {b_fmt} = {result}"
    except Exception:
        pass
    return None

# ── Default Responses ────────────────────────────────────────
default_responses = [
    "Hmm, I'm not sure about that 🤔 Can you rephrase?",
    "Interesting! Could you tell me more? 💬",
    "I didn't catch that. Try typing 'help' to see what I can do!",
    "That's beyond my current knowledge, but I'm always learning! 😊",
    "Not sure I understand — try rephrasing! 🤖",
    "Oops! That went over my circuits 😅 Try asking differently."
]

# ── Get Response (case-insensitive matching) ─────────────────
def get_response(user_input):
    text = user_input.strip()

    # Math check
    math_result = try_math(text)
    if math_result:
        return math_result

    # Intent matching (case-insensitive)
    for intent_name, intent_data in intents.items():
        pattern  = intent_data["patterns"]
        response = intent_data["responses"]

        if re.search(pattern, text, re.IGNORECASE):
            chosen = random.choice(response)

            # Dynamic responses
            if chosen == "__TIME__":
                return f"🕐 Current time: {datetime.now().strftime('%I:%M:%S %p')}"
            if chosen == "__DATE__":
                return f"📅 Today is {datetime.now().strftime('%A, %d %B %Y')}"
            if chosen == "__HISTORY__":
                return show_history()

            return chosen

    return random.choice(default_responses)

# ── Exit Check ───────────────────────────────────────────────
def is_exit(text):
    return bool(re.search(r"\bbye\b|\bgoodbye\b|\bexit\b|\bquit\b|\bsee you\b|\bsee ya\b|\bfarewell\b", text, re.IGNORECASE))

# ── Welcome Banner ───────────────────────────────────────────
def print_banner():
    print(Colors.CYAN + Colors.BOLD)
    print("╔══════════════════════════════════════════════════╗")
    print("║           🤖  CodBot v3.0  🤖                   ║")
    print("║   CodSoft Artificial Intelligence Internship    ║")
    print("║   Author  : Varad Abhijeet Gadekar              ║")
    print("║   Batch   : March B87                           ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  Try: 'help' | 'joke' | 'fun fact' | '5 + 3'   ║")
    print("║  Try: 'what is AI' | 'motivate me' | 'bye'      ║")
    print("╚══════════════════════════════════════════════════╝")
    print(Colors.RESET)

# ── Example Conversation (shown at start) ───────────────────
def print_example():
    print(Colors.YELLOW + "── Example Conversation ──────────────────────────")
    print("  You    : hello")
    print("  CodBot : Hello! I'm CodBot v3.0. How can I help?")
    print("  You    : what is AI")
    print("  CodBot : AI is the simulation of human intelligence...")
    print("  You    : 25 + 17")
    print("  CodBot : 🧮 25 + 17 = 42")
    print("  You    : tell me a joke")
    print("  CodBot : Why do programmers prefer dark mode?...")
    print("  You    : bye")
    print("  CodBot : Goodbye! Have an amazing day! 👋")
    print("──────────────────────────────────────────────────" + Colors.RESET)
    print()

# ── Main Chat Loop ───────────────────────────────────────────
def main():
    print_banner()
    print_example()

    while True:
        try:
            user_input = input(Colors.GREEN + "You    : " + Colors.RESET).strip()
        except (EOFError, KeyboardInterrupt):
            print(Colors.YELLOW + "\nCodBot : Goodbye! 👋 Take care!" + Colors.RESET)
            break

        if not user_input:
            print(Colors.YELLOW + "CodBot : Please say something! 😊\n" + Colors.RESET)
            continue

        # Save to history
        save_history("You", user_input)

        # Check exit first
        if is_exit(user_input):
            response = random.choice([
                "Goodbye! Have an amazing day! 👋😊",
                "Bye bye! Come back anytime! 🤖💙",
                "Farewell! Keep coding and stay awesome! 🚀"
            ])
            print(Colors.CYAN + f"CodBot : {response}\n" + Colors.RESET)
            save_history("CodBot", response)
            break

        # Get and print response
        response = get_response(user_input)
        print(Colors.CYAN + f"CodBot : {response}\n" + Colors.RESET)
        save_history("CodBot", response)

if __name__ == "__main__":
    main()
