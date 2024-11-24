from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import re

API_TOKEN = "8020902437:AAFVHa34mgJ0l5HH4K3h2ZahTMmtP3DSS7Y"
ADMIN_ID = 893646369  # Ваш Telegram ID

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Цены"), KeyboardButton(text="🚚 Доставка")],
        [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="✍️ Отзыв")],
        [KeyboardButton(text="🛒 Заказать")],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Добро пожаловать в CaviarKingBot! 🍣\n"
        "Здесь вы найдёте лучшую красную икру:\n"
        "🛍 Горбуши и Кеты.\n\n"
        "Выберите интересующий вас раздел из меню ниже:",
        reply_markup=main_menu,
    )



# Обработка кнопки "💵 Цены"
@dp.message(lambda message: message.text == "💵 Цены")
async def show_prices(message: Message):
    await message.answer(
        "Цены:\n"
        "📌 Горбуша: 8500 руб/кг.\n"
        "📌 Кета: 9000 руб/кг.\n"
        "Доставка — бесплатно при заказе от 1 кг.!"
    )

# Обработка кнопки "🚚 Доставка"
@dp.message(lambda message: message.text == "🚚 Доставка")
async def show_delivery(message: Message):
    await message.answer(
        "Мы доставляем:\n"
        "🚗 По Москве и МО — 2-5 дней.\n"
        "Доставка — бесплатно при заказе от 1 кг.!"
    )

# Обработка кнопки "📞 Контакты"
@dp.message(lambda message: message.text == "📞 Контакты")
async def show_contacts(message: Message):
    await message.answer(
        "📱 Наши контакты:\n"
        "Телефон: +7(996)-670-29-62\n"
        "Телеграм: @mFilic"
    )

# Обработка кнопки "✍️ Отзывы"
@dp.message(lambda message: message.text == "✍️ Отзыв")
async def feedback(message: Message):
    await message.answer("Напишите ваш отзыв, и мы обязательно его учтём!")

# Обработка кнопки "🛒 Заказать"
@dp.message(lambda message: message.text == "🛒 Заказать")
async def start_order(message: Message):
    await message.answer(
        "Пожалуйста, укажите:\n"
        "1️⃣ Продукт (Кета или Горбуша)\n"
        "2️⃣ Количество (0.5 кг или 1 кг)\n"
        "3️⃣ Ваш номер телефона (например: 89165456785)\n"
        "4️⃣ Адрес доставки\n\n"
        "Например:\n"
        "Кета, 1 кг, 89165456785, ул. Пушкина, д. 10"
    )

# Проверка заказа
@dp.message(lambda message: re.match(r"^(кета|кеты|горбуша|горбуши)[^a-zA-Z]*", message.text, re.IGNORECASE))
async def process_order(message: Message):
    order_details = message.text
    # Отправляем заказ вам
    await bot.send_message(ADMIN_ID, f"Новый заказ от {message.from_user.full_name}:\n{order_details}")
    await message.answer("Мы получили заказ, в ближайшее время с Вами свяжемся!")

# Обработка отзыва (любое другое сообщение)
@dp.message(lambda message: not re.match(r"^(кета|горбуша)", message.text, re.IGNORECASE))
async def process_feedback(message: Message):
    await bot.send_message(ADMIN_ID, f"Новый отзыв от {message.from_user.full_name}:\n{message.text}")
    await message.answer("Спасибо за отзыв. Нам очень важно ваше мнение!")

# Ретрансляция всех сообщений пользователя в Telegram
@dp.message()
async def forward_user_message(message: Message):
    # Ретранслируем все сообщения в Telegram вам
    await bot.send_message(ADMIN_ID, f"Сообщение от {message.from_user.full_name} ({message.from_user.id}):\n{message.text}")

# Запуск бота
if __name__ == "__main__":
    import asyncio
    from aiogram import Dispatcher

    dp.run_polling(bot)