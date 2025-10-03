import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 6540509823  # ЗАМЕНИТЕ НА ВАШ РЕАЛЬНЫЙ ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎁 Магазин NFT", callback_data="shop")],
        [InlineKeyboardButton("💼 Мои сделки", callback_data="trades")],
    ]
    
    # Добавляем админ кнопку если это админ
    if user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🛠️ Админ панель", callback_data="admin")])
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в бота для сделок с NFT!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🎁 Управление NFT", callback_data="manage_nft")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    
    await query.edit_message_text(
        "🛠️ Панель администратора\n\n"
        "📊 Ваша статистика:\n"
        "• Сделок: 1423\n"
        "• Рейтинг: 5.0/5 ⭐⭐⭐⭐⭐\n"
        "💎 Баланс: Безлимитный\n\n"
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    stats_text = (
        "📊 Статистика системы\n\n"
        "👥 Пользователей: 15\n"
        "🎁 NFT товаров: 7\n"
        "💼 Активных сделок: 3\n"
        "💎 Ваш статус: АДМИНИСТРАТОР\n\n"
        "🛠️ Управление через админ панель"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]]
    await query.edit_message_text(stats_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "admin":
        await admin_panel(update, context)
    elif query.data == "admin_panel":
        await admin_panel(update, context)
    elif query.data == "stats":
        await admin_stats(update, context)
    elif query.data == "main_menu":
        await start(update, context)
    else:
        await query.edit_message_text("⚙️ Функция в разработке...")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Тестовая команда работает!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Доступные команды:\n"
        "/start - Главное меню\n"
        "/test - Тест бота\n"
        "/help - Помощь"
    )

def main():
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        print("🔧 Убедитесь что переменная BOT_TOKEN установлена в Render")
        return
    
    try:
        # Создаем Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("test", test_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Запускаем бота
        print("🤖 Бот запускается...")
        print(f"✅ Токен получен: {BOT_TOKEN[:10]}...")
        
        print("🔄 Запускаем опрос...")
      application.run_polling()
        print("✅ Бот успешно запущен!")
        
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
