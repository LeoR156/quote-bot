import os

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения TOKEN не задана!")

admin_ids_raw = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS = {int(i) for i in admin_ids_raw.split(",") if i.strip()}
