import os
import requests
import time
from dotenv import load_dotenv
import re

# Load Mistral API key from .env
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# System prompt for topic classification (single output)
TOPIC_SYSTEM_PROMPT = (
    "You are an AI assistant. Your job is to analyze a list of exam questions "
    "and return only the 5 to 6 most frequently occurring or important *topics*. "
    "Do not list topics question by question. Do not give answers. Do not repeat questions. "
    "Just output the most common high-level *topics* that the questions are based on. "
    "Avoid subject names like 'Computer Science' or 'Mathematics' — return specific technical or conceptual topics "
    "like 'Two-Way Data Binding', 'Stream Piping', or 'Form Validation'."
)

def tag_topic(all_questions_text):
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": TOPIC_SYSTEM_PROMPT},
            {"role": "user", "content": all_questions_text}
        ],
        "temperature": 0.2
    }
    try:
        response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return "Unknown"
    except Exception as e:
        print("❌ Request failed:", e)
        return "Unknown"

def load_important_questions(file_path="important_questions.txt"):
    questions = []
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return questions
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            q = line.strip()
            if q:
                questions.append(q)
    return questions

def tag_and_print_topics(questions):
    print(f"\n🧠 Sending {len(questions)} important questions to Mistral...\n")
    
    combined_text = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
    raw_response = tag_topic(combined_text)

    # Clean response
    cleaned_lines = [
        re.sub(r"^[*•#\-\d.\s]+", "", line).strip()
        for line in raw_response.splitlines()
        if line.strip()
    ]

    print("🔥 Top Common Topics:")
    for topic in cleaned_lines:
        print(f"• {topic}")

#for testing (i dont forget to remove this lines) :)

# if __name__ == "__main__":
#     important_questions = load_important_questions("important_questions.txt")
#     if important_questions:
#         tag_and_print_topics(important_questions)
#     else:
#         print("⚠️ No questions found to process.")
