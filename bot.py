import os
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💰 Баланс", callback_data="balance"),
            InlineKeyboardButton("🟡 Купить Gold", callback_data="buy"),
        ],
        [
            InlineKeyboardButton("🎁 Кейсы", callback_data="cases"),
            InlineKeyboardButton("💸 Вывод", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton("📜 История", callback_data="history"),
            InlineKeyboardButton("🆘 Поддержка", callback_data="support"),
        ],
    ]

    await update.message.reply_text(
        "🟡 Добро пожаловать в Sellholic!\n\n"
        "Выбери нужный раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    responses = {
        "balance": "🟡 Твой баланс: 0 Gold",
        "buy": "🟡 Покупка Gold\n\nПакеты Gold скоро появятся.",
        "cases": "🎁 Кейсы\n\nКейсы скоро появятся.",
        "withdraw": "💸 Вывод Gold\n\nМинимальная сумма: 100 Gold.",
        "history": "📜 История пока пустая.",
        "support": "🆘 Поддержка\n\nРаздел поддержки скоро будет доступен.",
    }

    await query.message.reply_text(
        responses.get(query.data, "Неизвестная команда.")
    )


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Sellholic bot запущен!")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
