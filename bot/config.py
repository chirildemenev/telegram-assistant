import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tasks.db")

# Рабочая модель
GEMINI_MODEL = "gemini-2.5-flash"
MAX_HISTORY = 10

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден!")