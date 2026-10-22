import requests
from django.conf import settings

def send_telegram_message(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_ADMIN_CHAT_ID

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )

        print("HTTP status:", response.status_code)
        print("Telegram response:", response.json())

        response.raise_for_status()
        result = response.json()
        return result.get("ok", False)

    except requests.RequestException as error:
        print("Request error:", error)
        return False

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

def verify_telegram_init_data(init_data, max_age=86400):
    token = settings.TELEGRAM_BOT_TOKEN

    if not init_data or not token:
        return None

    try:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = parsed.pop("hash", None)

        if not received_hash:
            return None

        # Формируем строку, которую подписал Telegram.
        data_check_string = "\n".join(
            f"{key}={value}"
            for key, value in sorted(parsed.items())
        )

        # Секретный ключ для проверки подписи Telegram.
        secret_key = hmac.new(
            b"WebAppData",
            token.encode(),
            hashlib.sha256,
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(calculated_hash, received_hash):
            return None

        auth_date = int(parsed.get("auth_date", "0"))

        if auth_date <= 0 or time.time() - auth_date > max_age:
            return None

        user_data = json.loads(parsed.get("user", "{}"))
        user_id = user_data.get("id")

        if not isinstance(user_id, int) or isinstance(user_id, bool):
            return None

        return user_id

    except (ValueError, TypeError, json.JSONDecodeError):
        return None
