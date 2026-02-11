
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command

TOKEN = "8590754440:AAH4Xb_WuQVy2Z8a1oJEozpEtApByVtgxV8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Кнопки ---
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Запуск")]],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Расписание")],
        [KeyboardButton(text="👤 Мой профиль")]
    ],
    resize_keyboard=True
)

# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Готов к работе!\nНажмите «Запуск»!",
        reply_markup=start_keyboard
    )

# --- Запуск ---
@dp.message(F.text == "🚀 Запуск")
async def launch(message: Message):
    await message.answer(
        "Главное меню 👇",
        reply_markup=main_menu
    )

# --- Расписание ---
@dp.message(F.text == "📅 Расписание")
async def schedule(message: Message):
    text = (
        "📚 *Ваше расписание*\n\n"
        "Понедельник:\n"
        "09:00 — Математика\n"
        "11:00 — Информатика\n\n"
        "Вторник:\n"
        "10:00 — Физика\n"
        "12:00 — История\n"
    )
    await message.answer(text, parse_mode="Markdown")

# --- Профиль ---
@dp.message(F.text == "👤 Мой профиль")
async def profile(message: Message):
    avatar = FSInputFile("avatar.jpg")

    profile_text = (
        "👤 *Профиль пользователя*\n\n"
        "ФИО: Иванов Иван Иванович\n"
        "Статус: Студент\n"
        "Комментарий: Люблю IT и технологии 🚀"
    )

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=avatar,
        caption=profile_text,
        parse_mode="Markdown"
    )

# --- Запуск бота ---
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






























