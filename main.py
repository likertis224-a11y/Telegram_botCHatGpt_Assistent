
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from openai import OpenAI

TOKEN = "8590754440:AAH4Xb_WuQVy2Z8a1oJEozpEtApByVtgxV8"

bot = Bot(token=TOKEN)
# Используем MemoryStorage для хранения состояний и задач (в памяти)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Инициализация OpenAI клиента через Replit AI Integrations
# Не требует своего API ключа, оплата списывается с ваших кредитов Replit
client = OpenAI(
    base_url="https://api.replit.com/ai/v1",
    api_key=os.environ.get("REPLIT_API_KEY"),
)

# Временное хранилище задач в памяти (в продакшене лучше БД)
user_tasks = {}

class TaskStates(StatesGroup):
    waiting_for_task_text = State()
    waiting_for_ai_prompt = State()

# --- Кнопки ---
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Запуск")]],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Расписание"), KeyboardButton(text="👤 Мой профиль")],
        [KeyboardButton(text="➕ Добавить задачу"), KeyboardButton(text="📋 Мои задачи")],
        [KeyboardButton(text="🤖 AI Помощник"), KeyboardButton(text="🔗 Ссылки")],
        [KeyboardButton(text="📝 Заметки"), KeyboardButton(text="❓ FAQ")],
        [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="🔄 В начало (/start)")]
    ],
    resize_keyboard=True
)

# --- Команда /start ---
@dp.message(F.text == "🔄 В начало (/start)")
@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я твой помощник.\nИспользуйте меню ниже для навигации.",
        reply_markup=main_menu
    )

# --- Запуск ---
@dp.message(F.text == "🚀 Запуск")
@dp.message(Command("menu"))
async def launch(message: Message):
    await message.answer(
        "Главное меню 👇\nИспользуйте кнопки для навигации.",
        reply_markup=main_menu
    )

# --- AI Помощник ---
@dp.message(F.text == "🤖 AI Помощник")
@dp.message(Command("ai"))
async def ai_start(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_ai_prompt)
    await message.answer("🤖 Я готов помочь! Введите ваш вопрос или промпт для ChatGPT:")

@dp.message(TaskStates.waiting_for_ai_prompt)
async def process_ai_prompt(message: Message, state: FSMContext):
    prompt = message.text
    msg = await message.answer("⌛ Думаю...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты полезный ассистент для студента."},
                {"role": "user", "content": prompt}
            ],
        )
        answer = response.choices[0].message.content
        await msg.edit_text(answer)
    except Exception as e:
        await msg.edit_text(f"❌ Произошла ошибка при обращении к AI: {str(e)}")
    
    await state.clear()

# --- Добавление задачи ---
@dp.message(F.text == "➕ Добавить задачу")
async def add_task_start(message: Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_task_text)
    await message.answer("✍️ Введите текст задачи, которую нужно сохранить:")

@dp.message(TaskStates.waiting_for_task_text)
async def process_task_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    task_text = message.text
    
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    
    user_tasks[user_id].append(task_text)
    
    await state.clear()
    await message.answer(f"✅ Задача сохранена: \"{task_text}\"", reply_markup=main_menu)

# --- Список задач ---
@dp.message(F.text == "📋 Мои задачи")
@dp.message(Command("tasks"))
async def show_tasks(message: Message):
    user_id = message.from_user.id
    tasks = user_tasks.get(user_id, [])
    
    if not tasks:
        await message.answer("📭 У вас пока нет сохраненных задач.")
    else:
        tasks_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
        await message.answer(f"📋 *Ваши задачи:*\n\n{tasks_list}", parse_mode="Markdown")

# --- Расписание ---
@dp.message(F.text == "📅 Расписание")
@dp.message(Command("schedule"))
async def schedule(message: Message):
    text = (
        "📚 *Ваше полное расписание на неделю:*\n\n"
        "📅 *Понедельник*\n"
        "1. 09:00 — Математика\n"
        "2. 10:40 — Информатика\n"
        "3. 12:40 — Английский язык\n"
        "4. 14:20 — Физическая культура\n"
        "5. 16:00 — Дискретная математика\n\n"
        "📅 *Вторник*\n"
        "1. 09:00 — Основы программирования\n"
        "2. 10:40 — Архитектура ЭВМ\n"
        "3. 12:40 — История\n"
        "4. 14:20 — Линейная алгебра\n"
        "5. 16:00 — Психология\n\n"
        "📅 *Среда*\n"
        "1. 09:00 — Базы данных\n"
        "2. 10:40 — Сетевые технологии\n"
        "3. 12:40 — Философия\n"
        "4. 14:20 — Операционные системы\n"
        "5. 16:00 — Иностранный язык (проф.)\n"
        "6. 17:40 — Факультатив по Python\n\n"
        "📅 *Четверг*\n"
        "1. 09:00 — Веб-разработка (Frontend)\n"
        "2. 10:40 — Алгоритмы и структуры данных\n"
        "3. 12:40 — Культурология\n"
        "4. 14:20 — Физика\n"
        "5. 16:00 — Правоведение\n\n"
        "📅 *Пятница*\n"
        "1. 09:00 — Объектно-ориентированное программирование\n"
        "2. 10:40 — Безопасность жизнедеятельности\n"
        "3. 12:40 — Экономика\n"
        "4. 14:20 — Статистика\n"
        "5. 16:00 — Тестирование ПО\n"
        "6. 17:40 — Лабораторная работа\n\n"
        "💡 *Совет:* Хорошего дня и продуктивной учебы!"
    )
    await message.answer(text, parse_mode="Markdown")

# --- Профиль ---
@dp.message(F.text == "👤 Мой профиль")
@dp.message(Command("profile"))
async def profile(message: Message):
    avatar = FSInputFile("avatar.jpg")

    profile_text = (
        "👤 *Профиль пользователя*\n\n"
        "🆔 ID: `{}`\n"
        "👤 Имя: {}\n"
        "🎓 Статус: Студент\n"
        "📝 О себе: Люблю IT и технологии 🚀"
    ).format(message.from_user.id, message.from_user.full_name)

    try:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=avatar,
            caption=profile_text,
            parse_mode="Markdown"
        )
    except Exception:
        await message.answer(profile_text, parse_mode="Markdown")

# --- Ссылки ---
@dp.message(F.text == "🔗 Ссылки")
@dp.message(Command("links"))
async def links(message: Message):
    text = (
        "🔗 *Полезные ссылки:*\n\n"
        "🌐 [Сайт университета](https://example.com)\n"
        "📖 [Электронная библиотека](https://example.com/lib)\n"
        "💬 [Чат группы](https://t.me/example_group)\n"
        "📂 [Материалы лекций](https://example.com/materials)"
    )
    await message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

# --- Заметки ---
@dp.message(F.text == "📝 Заметки")
@dp.message(Command("notes"))
async def notes(message: Message):
    text = (
        "📝 *Ваши текущие задачи:*\n\n"
        "✅ Сдать проект по Python\n"
        "⏳ Прочитать главу 5 по истории\n"
        "❌ Подготовиться к тесту по физике\n\n"
        "ℹ️ _Функция добавления заметок будет доступна скоро!_"
    )
    await message.answer(text, parse_mode="Markdown")

# --- FAQ ---
@dp.message(F.text == "❓ FAQ")
@dp.message(Command("faq"))
async def faq(message: Message):
    text = (
        "❓ *Часто задаваемые вопросы:*\n\n"
        "1️⃣ *Где найти кабинет?* — Карта доступна в холле 1 этажа.\n"
        "2️⃣ *Как заказать справку?* — Через личный кабинет на сайте.\n"
        "3️⃣ *Когда каникулы?* — С 1 по 14 июля.\n"
        "4️⃣ *Как сменить пароль от Wi-Fi?* — Обратитесь в ИТ-отдел."
    )
    await message.answer(text, parse_mode="Markdown")

# --- Контакты ---
@dp.message(F.text == "📞 Контакты")
@dp.message(Command("contacts"))
async def contacts(message: Message):
    text = (
        "📞 *Важные контакты:*\n\n"
        "🏢 *Деканат:* +7 (999) 000-11-22\n"
        "👨‍🏫 *Куратор:* @username\n"
        "🛠 *Техподдержка:* @it_support_bot\n"
        "📧 *Email:* support@university.edu"
    )
    await message.answer(text, parse_mode="Markdown")

# --- Запуск бота ---
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

