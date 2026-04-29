# Tạo service đọc config session
import json

from app.core.config import SESSION_CONFIG_PATH


class ConfigService:
    def load_session_config(self):
        if not SESSION_CONFIG_PATH.exists():
            raise FileNotFoundError(f"Không tìm thấy file config: {SESSION_CONFIG_PATH}")

        with open(SESSION_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)