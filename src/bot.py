import logging

from telebot import TeleBot
from telebot.types import Message

from .config import TOKEN, ADMIN_IDS
from .quotes import get_random_quote, add_quote, count_quotes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

bot = TeleBot(TOKEN)


# ─── Хэндлеры ────────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start"])
def cmd_start(message: Message):
    name = message.from_user.first_name
    bot.reply_to(
        message,
        f"Привет, {name}! 👋\n\n"
        "Я бот с цитатами. Вот что я умею:\n"
        "/quote — случайная цитата\n"
        "/stats — сколько цитат в базе\n"
        "/add <текст> — добавить цитату (только для администратора)",
    )
    logging.info(f"[/start] user_id={message.from_user.id} ({message.from_user.first_name})")


@bot.message_handler(commands=["quote"])
def cmd_quote(message: Message):
    quote = get_random_quote()
    if quote is None:
        bot.reply_to(message, "😔 Цитат пока нет. Попросите администратора добавить хотя бы одну!")
    else:
        bot.reply_to(message, f"💬 {quote}")
    logging.info(f"[/quote] user_id={message.from_user.id}")


@bot.message_handler(commands=["stats"])
def cmd_stats(message: Message):
    total = count_quotes()
    bot.reply_to(message, f"📚 В базе {total} цитат.")
    logging.info(f"[/stats] user_id={message.from_user.id}, total={total}")


@bot.message_handler(commands=["add"])
def cmd_add(message: Message):
    # Проверяем права
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "🚫 У вас нет прав для добавления цитат.")
        logging.warning(f"[/add] Unauthorized attempt by user_id={message.from_user.id}")
        return

    # Извлекаем текст после команды /add
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        bot.reply_to(message, "✏️ Укажите текст цитаты. Пример:\n/add Жизнь прекрасна!")
        return

    quote_text = parts[1].strip()
    added = add_quote(quote_text)

    if added:
        bot.reply_to(message, f"✅ Цитата добавлена:\n\n💬 {quote_text}")
        logging.info(f"[/add] Added new quote by user_id={message.from_user.id}")
    else:
        bot.reply_to(message, "⚠️ Такая цитата уже есть в базе.")


# ─── Точка входа ─────────────────────────────────────────────────────────────

def main():
    logging.info("Бот запущен в режиме polling...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
