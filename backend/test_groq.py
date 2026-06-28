import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "hello"}],
        model="llama-3.3-70b-versatile",
    )
    print("SUCCESS: Key is valid!")
except Exception as e:
    print(f"FAILED: {e}")
