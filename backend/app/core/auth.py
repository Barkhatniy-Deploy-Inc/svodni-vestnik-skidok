import hmac
import hashlib
import json
from urllib.parse import parse_qs, unquote
from fastapi import Header, HTTPException, Depends
from typing import Optional
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def verify_telegram_data(init_data: str) -> Optional[int]:
    """
    Проверяет подлинность данных Telegram и возвращает user_id.
    """
    if not init_data or not BOT_TOKEN:
        return None

    try:
        vals = {k: unquote(v[0]) for k, v in parse_qs(init_data).items()}
        hash_str = vals.pop('hash', None)
        user_str = vals.get('user')
        
        if not hash_str or not user_str:
            return None

        # Проверка хеша
        data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(vals.items())])
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != hash_str:
            return None

        # Извлечение ID пользователя
        user_data = json.loads(user_str)
        return user_data.get('id')
    except Exception:
        return None

async def get_current_user_id(x_tg_data: Optional[str] = Header(None)):
    """
    Зависимость для защиты эндпоинтов.
    """
    if not x_tg_data:
        raise HTTPException(status_code=401, detail="Отсутствуют данные авторизации")
        
    user_id = verify_telegram_data(x_tg_data)
    if not user_id:
        raise HTTPException(status_code=401, detail="Неверная подпись данных")
    
    return user_id
