import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

# Replace with your Mistral API key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"


HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# LLM prompt to clean up raw exam text
SYSTEM_PROMPT = """
You are a helpful assistant that extracts only the actual exam questions from raw exam paper text.

Instructions:

1. Completely ignore headers, footers, metadata, instructions, marks, and page numbers.
2. Remove all question numbers like Q1, Q.1, Q-1, 1., 1), Question 1, etc.
3. Remove all separator keywords like OR, AND, CHOOSE ANY ONE, etc.
4. If a question has multiple parts or examples, merge them into one complete question in a single line.
   - Do NOT break sub-parts into separate questions.
   - Keep all context (e.g., logic statements, examples) together with the main question.
5. Output only clean full questions — one per line.
6. Do NOT number the questions in your output at all. Just plain text questions, each on its own line.
"""


def send_to_mistral(chunk):
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": chunk}
        ],
        "temperature": 0.2,
    }

    response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("❌ Error:", response.status_code, response.text)
        return ""

def chunk_text(text, max_words=200):  # ~4000 tokens
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def process_all_texts(input_folder="extracted_texts", output_folder="clean_questions"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            print(f"🔍 Processing {filename}...")

            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            chunks = chunk_text(raw_text)
            all_cleaned = ""

            for i, chunk in enumerate(chunks):
                print(f"  → Sending chunk {i+1}/{len(chunks)}")
                cleaned = send_to_mistral(chunk)
                all_cleaned += cleaned + "\n\n"
                time.sleep(1.5)  # Avoid rate limits

            # Save output
            out_filename = filename.replace(".txt", "_cleaned.txt")
            out_path = os.path.join(output_folder, out_filename)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(all_cleaned)

            print(f"✅ Cleaned questions saved to {out_path}")

# Run the cleaner

