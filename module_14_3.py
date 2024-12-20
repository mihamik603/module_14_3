from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Рассчитать", "Информация", "Купить"]  # Добавлена кнопка "Купить"
    keyboard.add(*buttons)
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Купить')
async def get_buying_list(message: types.Message):
    products = [
        {"name": "Product1", "description": "Описание 1", "price": 100, "image": 'C:\\Users\\Михалыч\\PycharmProjects\\pythonProject5\\Product1.jpg'},
        {"name": "Product2", "description": "Описание 2", "price": 200, "image": 'C:\\Users\\Михалыч\\PycharmProjects\\pythonProject5\\Product2.jpg'},
        {"name": "Product3", "description": "Описание 3", "price": 300, "image": 'C:\\Users\\Михалыч\\PycharmProjects\\pythonProject5\\Product3.jpg'},
        {"name": "Product4", "description": "Описание 4", "price": 400, "image": 'C:\\Users\\Михалыч\\PycharmProjects\\pythonProject5\\Product4.jpg'},
    ]

    for product in products:
        await message.answer(
            f'Название: {product["name"]} | Описание: {product["description"]} | Цена: {product["price"]}')
        await message.answer_photo(photo=open(product["image"], 'rb'))

    inline_keyboard = InlineKeyboardMarkup()
    for product in products:
        inline_keyboard.add(InlineKeyboardButton(product["name"], callback_data="product_buying"))
    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.errors_handler()
async def error_handler(update, exception):
    print(f'Произошла ошибка: {exception}')
    return True 

@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
