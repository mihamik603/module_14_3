from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8084154106:AAHn3ikCWbQ8Knky3VxfujNvgu8VgFTNTWQ'

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


@dp.message_handler(lambda message: message.text == 'Купить')  # Хэндлер для кнопки "Купить"
async def get_buying_list(message: types.Message):
    products = [
        {"name": "Product1", "description": "описание 1", "price": 100},
        {"name": "Product2", "description": "описание 2", "price": 200},
        {"name": "Product3", "description": "описание 3", "price": 300},
        {"name": "Product4", "description": "описание 4", "price": 400},
    ]

    for product in products:
        await message.answer(
            f'Название: {product["name"]} | Описание: {product["description"]} | Цена: {product["price"]}')
        # Здесь можно добавить код для отправки изображений, например:
        # await message.answer_photo(photo='URL_картинки_продукта')

    inline_keyboard = InlineKeyboardMarkup()
    for product in products:
        inline_keyboard.add(InlineKeyboardButton(product["name"], callback_data='product_buying'))

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == 'product_buying')  # Хэндлер для покупки продукта
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def main_menu(message: types.Message):
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(
        InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories'),
        InlineKeyboardButton("Формулы расчёта", callback_data='formulas')
    )
    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5\n"
        "Для женщин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) - 161"
    )
    await call.message.answer(formula_message)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()
    await call.message.answer("Введите свой возраст:")
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer("Введите свой рост:")


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer("Введите свой вес:")


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
    await state.finish()


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
