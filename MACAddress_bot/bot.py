import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler

FIRST_MESSAGE, SECOND_MESSAGE, SHOW_ALL = range(3)
ALLOWED_USERS = [429394445]

# Декоратор для проверки доступа
def restricted(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            if update.callback_query:
                await update.callback_query.answer("У вас нет доступа!", show_alert=True)
            else:
                await update.message.reply_text("У вас нет доступа!")
            return ConversationHandler.END
        return await func(update, context, *args, **kwargs)
    return wrapper

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

# Главное меню с кнопками
async def show_main_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Добавить MAC-адрес", callback_data='add')],
        [InlineKeyboardButton("Посмотреть этапы", callback_data='stages')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:  # Если команда вызвана через /start
        await update.message.reply_text("Что вы хотите сделать?:", reply_markup=reply_markup)
    elif update.callback_query:  # Если завершение сценария через callback
        await update.callback_query.message.edit_text("Что вы хотите сделать?:", reply_markup=reply_markup)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Этот бот создан для формирования базы с информацией об экранах.")
    await show_main_menu(update, context)

@restricted
async def show_all(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await show_main_menu(update, context)
    return ConversationHandler.END

# Обработчик кнопки "Добавить MAC-адрес"
async def add_mac_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Введите серийный номер")
    return FIRST_MESSAGE

# Обработка серийного номера
async def first_message(update: Update, context: CallbackContext) -> int:
    context.user_data['serial_number'] = update.message.text
    await update.message.reply_text("Введите MAC-адрес")
    return SECOND_MESSAGE

# Обработка MAC-адреса
async def second_message(update: Update, context: CallbackContext) -> int:
    num = context.user_data['serial_number']
    mac = update.message.text
    save_message(num, mac)
    await update.message.reply_text(f"Информация сохранена:\nСерийный номер: {num}\nMAC-адрес: {mac}")
    # Вернуться в главное меню
    await show_main_menu(update, context)
    return ConversationHandler.END

@restricted
# Обработчик кнопки "Посмотреть этапы"
async def stages_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    # Здесь можно добавить логику отображения этапов
    await query.edit_message_text("Этапы:\n1. Ввод серийного номера\n2. Ввод MAC-адреса\n3. Сохранение в базу данных")
    # Вернуться в главное меню
    await show_main_menu(update, context)
    return SHOW_ALL

# Обработчик отмены
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Ввод информации прекращен.")
    await show_main_menu(update, context)
    return ConversationHandler.END

def main():
    # Токен вашего бота
    token = "7927932585:AAHzdL9aQKdD9qHtY0mzm6374m716PvUFXI"

    # Создаем базу данных и таблицу (если нужно)
    create_table()

    # Создаем объект Application
    application = Application.builder().token(token).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # ConversationHandler для добавления MAC-адреса
    add_mac_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_mac_handler, pattern="^add$")],
        states={
            FIRST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_message)],
            SECOND_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_message)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CallbackQueryHandler(stages_handler, pattern="^stages$"))

    # Добавляем ConversationHandler в приложение
    application.add_handler(add_mac_conversation)

    # Запуск бота
    application.run_polling()  # Эта строка запускает бота и держит процесс активным

if __name__ == "__main__":
    main()
