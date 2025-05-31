import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:********@********:****/smart-closet")

# API-ключи
OPENAI_API_KEY = os.getenv("********")

OPENAI_API_KEYY = "********"
ESP_DISPLAY_IP = os.getenv("ESP_DISPLAY_IP", "http://********")

OPENWEATHER_API_KEY = "********"

# Другие настройки
APP_NAME = "Smart Closet"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

HUGGINGFACE_API_KEY = "********"
SEGMIND_API_KEY = "********"
TEST_PERSON_IMAGE_URL = "********"