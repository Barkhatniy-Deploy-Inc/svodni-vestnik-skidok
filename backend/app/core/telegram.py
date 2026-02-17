import httpx
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Токен бота берется строго из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def send_notification(telegram_id: int, message: str) -> bool:
    """
    Отправляет текстовое сообщение пользователю в Telegram.
    Использует контекстный менеджер для клиента для повышения производительности.
    """
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не настроен в переменных окружения")
        return False

    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        # В будущем рекомендуется использовать долгоживущий клиент, 
        # но сейчас мы гарантируем закрытие соединения
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, json=payload)
            if response.status_code != 200:
                logger.error(f"Ошибка отправки сообщения в ТГ: {response.text}")
                return False
            return True
    except httpx.RequestError as e:
        logger.error(f"Ошибка сети при отправке уведомления в ТГ: {e}")
        return False
    except Exception as e:
        logger.error(f"Непредвиденное исключение при отправке сообщения: {e}", exc_info=True)
        return False
