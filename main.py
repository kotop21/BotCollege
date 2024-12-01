import logging
import datetime
import requests
import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import TOKEN
from colorama import Fore, Style, init

# Ініціалізація colorama
init(autoreset=True)

# Налаштування логування
logging.basicConfig(
    format=f"%(asctime)s - {Fore.GREEN}%(levelname)s{Style.RESET_ALL} - %(message)s",
    level=logging.INFO,
)

# Вимкнення логів HTTP-запитів Telegram
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

# Функція для отримання сьогоднішньої дати в потрібному форматі
def get_today_date():
    return datetime.datetime.today().strftime('%d.%m.%Y')

# Функція для отримання попередніх днів до сьогоднішнього
def get_previous_dates():
    today = datetime.datetime.today()
    dates = []
    for i in range(7):  # Перевіряємо 7 останніх днів
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%d.%m.%Y'))
    return dates

# Функція для скачування файлу з зміненою датою і курсом
def download_file(course_number, date):
    url = f"https://ztk.org.ua/files/{course_number}-{date}.pdf"
    logging.info(f"{Fore.CYAN}📥 Запит URL: {url}{Style.RESET_ALL}")
    response = requests.get(url)
    if response.status_code == 200:
        file_bytes = io.BytesIO(response.content)
        return file_bytes, date
    else:
        return None, None

# Обробка натискання на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    try:
        await query.answer()

        course = query.data
        dates = get_previous_dates()  # Отримуємо список останніх доступних дат
        today_date = get_today_date()

        # Початкове повідомлення з анімацією завантаження
        await query.edit_message_text(
            text=f"⏳ Завантаження розкладу для {course} курсу... Будь ласка, зачекайте. 📅",
            parse_mode='Markdown'
        )

        # Шукаємо перший доступний файл для курсу
        for date in dates:
            file, file_date = download_file(course, date)
            if file:
                if file_date == today_date:
                    await query.edit_message_text(
                        text=f"🎉 Завантаження розкладу для {course} курсу завершено! 📅\n\nНадсилаю файл...",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text(
                        text=f"⚠️ Сьогоднішній розклад відсутній. Надсилаю розклад за {file_date}. 📅",
                        parse_mode='Markdown'
                    )

                # Надсилаємо файл без збереження на сервері
                file.seek(0)  # Вказуємо на початок буфера перед відправкою
                await query.message.reply_document(file, filename=f"schedule_{course}_{file_date}.pdf")
                return

        # Якщо не знайдено розклад на останні 7 днів
        await query.edit_message_text(
            text="⚠️ Ой! Не вдалося знайти розклад за останні 7 днів. Спробуйте ще раз пізніше. 🙏",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"{Fore.RED}❌ Сталася помилка: {e}{Style.RESET_ALL}")
        await query.message.reply_text(
            text="⚠️ Виникла проблема при обробці запиту. Спробуйте пізніше. 🙏",
            parse_mode='Markdown'
        )

# Команда /start для привітання та відображення кнопок
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logging.info(f"{Fore.BLUE}👋 Користувач {user.full_name} (ID: {user.id}) запустив команду /start{Style.RESET_ALL}")

    keyboard = [
        [InlineKeyboardButton("1 курс 👶🏻", callback_data='1'), InlineKeyboardButton("2 курс 👦🏻", callback_data='2')],
        [InlineKeyboardButton("3 курс 👨🏻", callback_data='3'), InlineKeyboardButton("4 курс 👴🏻", callback_data='4')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text="👋 Привіт! Вибери курс для отримання розкладу. 📅\n\nАвтор бота: xxds🎀❤️‍🔥",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Головна функція
def main():
    application = Application.builder().token(TOKEN).build()

    # Команда /start
    application.add_handler(CommandHandler("start", start))

    # Обробка кнопок
    application.add_handler(CallbackQueryHandler(button))

    logging.info(f"{Fore.GREEN}🚀 Бот запущено та готовий до роботи!{Style.RESET_ALL}")
    application.run_polling()

if __name__ == '__main__':
    main()
