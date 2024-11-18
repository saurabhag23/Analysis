from dotenv import load_dotenv
import os

load_dotenv()

SEC_API_KEY = os.getenv("SEC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not SEC_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API keys are not set properly in the .env file.")
