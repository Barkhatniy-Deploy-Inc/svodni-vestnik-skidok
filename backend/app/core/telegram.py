import httpx
import logging
import os

logger = logging.getLogger(__name__)

# Токен бота берется из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_БОТА")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

async def send_notification(telegram_id: int, message: str):
    """
    Отправляет текстовое сообщение пользователю в Telegram.
    """
    payload = {
        "chat_id": telegram_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TELEGRAM_API_URL, json=payload)
            if response.status_code != 200:
                logger.error(f"Ошибка отправки сообщения в ТГ: {response.text}")
                return False
            return True
    except Exception as e:
        logger.error(f"Исключение при отправке сообщения: {e}")
        return False
