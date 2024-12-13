import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler

FIRST_MESSAGE, SECOND_MESSAGE = range(2)

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect('messages.db')

# Функция для создания таблицы (если еще не создана)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_number TEXT NOT NULL,
            MAC_address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для записи сообщения в базу данных
def save_message(num, mac: str):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO info (serial_number, MAC_address) VALUES (?, ?)', (num, mac))
        conn.commit()
    except sqlite3.OperationalError:
        print("Ошибка: база данных занята")
    finally:
        conn.close()

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Добавить", callback_data="add")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Этот бот создан для формирования базы с информацией об экранах. Выберите одну из функций ниже',
        reply_markup=reply_markup)
    return ConversationHandler.END

# Обработчик нажатия кнопки "Добавить"
async def button_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    # Уведомление, что процесс добавления начался
    await query.edit_message_text("Введите серийный номер изделия")
    return FIRST_MESSAGE

# Обработка первого сообщения (серийный номер)
async def first_message(update: Update, context: CallbackContext) -> int:
    context.user_data['serial_number'] = update.message.text
    await update.message.reply_text("Введите MAC-адрес")
    return SECOND_MESSAGE

# Обработка второго сообщения (MAC-адрес)
async def second_message(update: Update, context: CallbackContext) -> int:
    num = context.user_data['serial_number']
    mac = update.message.text
    save_message(num, mac)
    await update.message.reply_text(f"Информация сохранена:\nСерийный номер: {num}\nMAC-адрес: {mac}")
    keyboard = [
        [InlineKeyboardButton("Добавить", callback_data="add")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Что бы вы хотели сделать дальше?', reply_markup=reply_markup)
    return ConversationHandler.END

# Обработчик отмены
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Ввод информации прекращен")
    return ConversationHandler.END

def main():
    # Токен вашего бота
    token = "7927932585:AAHzdL9aQKdD9qHtY0mzm6374m716PvUFXI"

    # Создаем базу данных и таблицу (если нужно)
    create_table()

    # Создаем объект Application и передаем токен
    application = Application.builder().token(token).build()

    # Добавляем обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Определение ConversationHandler
    conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^add$")],
        states={
            FIRST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_message)],
            SECOND_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_message)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conversation)
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
