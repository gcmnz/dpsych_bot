import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BufferedInputFile
from aiogram.exceptions import TelegramBadRequest

from .api_token import API_TOKEN
from .keyboard import *
from .utils import *
from .database import *
from ..pdf import create_pdf

BASE_MESSAGE: str = "🧠 Цифровая психология"
INPUT_NAME: str = "👤 Введите имя (латиницей)"
INPUT_DATE: str = '📅 Введите дату в формате ДД.ММ.ГГГГ'
INCORRECT_NAME: str = '❌ Введено некорректное имя'
ACCOUNT_NOT_REGISTERED: str = "⚠️ Вы не зарегистрированы в системе\nУникальный идентификатор: <code>{}</code>"

INPUT_USER_IDENTIFER: str = '🆔 Введите уникальный идентификатор пользователя'
INCORRECT_IDENTIFER: str = '❌ Введён некорректный идентификатор'
U_ARE_NOT_ADMIN: str = '🔒 Не достаточно прав для выполнения данного действия'
USER_ADD_SUCCEED: str = '✅ Пользователь успешно добавлен'
USER_ALREADY_REGISTERED: str = '⚠️ Пользователь уже зарегистрирован'
USER_NOT_REGISTERED: str = '❌ Пользователь не зарегистрирован'
USER_DELETE_SUCCEED: str = '✅ Пользователь успешно удалён'
WAITING_FOR_FILE_GENERATION: str = '⏳ Файл создаётся, ожидайте...'


logging.basicConfig(level=logging.INFO)

db = Database("src/bot/database/users.db")
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


entered_name = {}  # Для хранения введённых данных {user_id: name}


class Form(StatesGroup):
    main_menu = State()
    send_name = State()
    send_date_of_birth = State()

    add_user = State()
    add_admin = State()
    delete_user = State()


@dp.message()
async def process_message(message: types.Message, state: FSMContext):

    message_text: str = message.text
    user_id: int = message.from_user.id

    if not await db.is_user_registered(user_id):
        await message.answer(ACCOUNT_NOT_REGISTERED.format(user_id), parse_mode='HTML')
        return

    current_state = await state.get_state()
    if current_state is None:
        current_state = Form.main_menu.state

    if current_state == Form.main_menu.state:
        if await db.is_user_admin(user_id):
            keyboard = admin_main_keyboard
        else:
            keyboard = generate_file_keyboard

        await message.answer(BASE_MESSAGE, reply_markup=keyboard)

    elif current_state == Form.send_name.state:
        if not is_valid_name(message.text):
            await message.answer(INCORRECT_NAME, reply_markup=back_keyboard)
            return

        entered_name[user_id] = message.text

        await message.answer(INPUT_DATE, reply_markup=back_keyboard)
        await state.set_state(Form.send_date_of_birth)

    elif current_state == Form.send_date_of_birth.state:
        if not is_valid_date(message.text):
            await message.answer(INPUT_DATE, reply_markup=back_keyboard)
            return

        name: str = entered_name[user_id]
        date: str = message.text
        del entered_name[user_id]

        await message.answer(WAITING_FOR_FILE_GENERATION)

        pdf_bytes, pdf_path = create_pdf(name=name, date_of_birth_str=date)
        pdf = BufferedInputFile(file=pdf_bytes, filename=pdf_path)

        if await db.is_user_admin(user_id):
            keyboard = admin_main_keyboard
        else:
            keyboard = generate_new_file_keyboard

        await bot.send_document(chat_id=user_id, document=pdf)
        await bot.send_message(chat_id=user_id, text=BASE_MESSAGE, reply_markup=keyboard)
        await db.increment_generate_file(user_id)

        await state.set_state(Form.main_menu)

    elif current_state == Form.add_user:
        if not await db.is_user_admin(user_id):
            await bot.send_message(chat_id=user_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard)
            await state.set_state(Form.main_menu)
            return

        if not await is_check_user_id_valid(message_text):
            await bot.send_message(chat_id=user_id, text=INCORRECT_IDENTIFER, reply_markup=back_keyboard)
            return

        userid: int = int(message_text)
        result: bool = await db.register_user(userid, await get_username_by_user_id(userid))
        if result:
            text: str = USER_ADD_SUCCEED
        else:
            text: str = USER_ALREADY_REGISTERED

        await state.set_state(Form.main_menu)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=admin_main_keyboard)
        await bot.send_message(chat_id=userid, text=BASE_MESSAGE, reply_markup=generate_file_keyboard)

    elif current_state == Form.add_admin:
        if not await db.is_user_admin(user_id):
            await bot.send_message(chat_id=user_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard)
            await state.set_state(Form.main_menu)
            return

        if not await is_check_user_id_valid(message_text):
            await bot.send_message(chat_id=user_id, text=INCORRECT_IDENTIFER, reply_markup=back_keyboard)
            return

        userid: int = int(message_text)
        result: bool = await db.register_user(userid, await get_username_by_user_id(userid), is_admin=True)
        if result:
            text: str = USER_ADD_SUCCEED
        else:
            text: str = USER_ALREADY_REGISTERED

        await state.set_state(Form.main_menu)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=admin_main_keyboard)
        await bot.send_message(chat_id=userid, text=BASE_MESSAGE, reply_markup=admin_main_keyboard)

    elif current_state == Form.delete_user:
        if not await db.is_user_admin(user_id):
            await bot.send_message(chat_id=user_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard)
            await state.set_state(Form.main_menu)
            return

        if not await is_check_user_id_valid(message_text):
            await bot.send_message(chat_id=user_id, text=INCORRECT_IDENTIFER, reply_markup=back_keyboard)
            return

        if not await db.is_user_registered(int(message_text)):
            await bot.send_message(chat_id=user_id, text=USER_NOT_REGISTERED, reply_markup=back_keyboard)
            return

        await db.delete_user(int(message_text))
        await bot.send_message(chat_id=user_id, text=USER_DELETE_SUCCEED, reply_markup=admin_main_keyboard)


@dp.callback_query(lambda c: c.data in ['generate_file', 'generate_new_file', 'back', 'add_user', 'add_admin', 'delete_user', 'load_database'])
async def process_callback_generate_file(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id: int = callback_query.from_user.id
    message_id: int = callback_query.message.message_id

    if callback_query.data == 'generate_file':
        await state.set_state(Form.send_name)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_NAME, reply_markup=back_keyboard)

    elif callback_query.data == 'generate_new_file':
        await state.set_state(Form.send_name)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_NAME, reply_markup=back_keyboard)

    elif callback_query.data == 'add_user':
        await state.set_state(Form.add_user)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_USER_IDENTIFER, reply_markup=back_keyboard)

    elif callback_query.data == 'add_admin':
        await state.set_state(Form.add_admin)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_USER_IDENTIFER, reply_markup=back_keyboard)

    elif callback_query.data == 'delete_user':
        await state.set_state(Form.delete_user)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_USER_IDENTIFER, reply_markup=back_keyboard)

    elif callback_query.data == 'load_database':
        if not await db.is_user_admin(chat_id):
            await bot.send_message(chat_id=chat_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard)
            return

        excel_buffer: bytes = await convert_db_to_excel(db)
        document = BufferedInputFile(file=excel_buffer, filename='users.xlsx')
        await bot.send_document(chat_id=chat_id, document=document)

        await bot.send_message(chat_id=chat_id, text=BASE_MESSAGE, reply_markup=admin_main_keyboard)

    elif callback_query.data == 'back':
        await process_back(state, chat_id, message_id)


async def process_back(state: FSMContext, chat_id: int, message_id: int) -> None:
    current_state = await state.get_state()

    if current_state == Form.send_date_of_birth.state:
        await state.set_state(Form.send_name)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_NAME, reply_markup=back_keyboard)
        return

    if current_state == Form.send_name.state or current_state == Form.add_user.state or current_state == Form.add_admin.state or current_state == Form.delete_user.state:
        await state.set_state(Form.main_menu)

        if await db.is_user_admin(chat_id):
            keyboard = admin_main_keyboard
        else:
            keyboard = generate_file_keyboard

        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=BASE_MESSAGE, reply_markup=keyboard)
        return


async def get_username_by_user_id(user_id: int) -> str | None:
    try:
        chat = await bot.get_chat(chat_id=user_id)
        return chat.username
    except Exception as e:
        print(f"Ошибка получения username (user_id: {user_id}): {e}")
        return None


async def is_check_user_id_valid(message_text: str) -> bool:
    if not message_text.isdigit():
        return False

    if await get_username_by_user_id(int(message_text)) is None:
        return False

    return True


async def send_greet_messages():
    ui_1 = 6859851833
    ui_2 = 1580689542
    # await db.register_user(tg_user_id=ui_1, tg_username=f"@{await get_username_by_user_id(ui_1)}", is_admin=True)
    await db.register_user(tg_user_id=ui_2, tg_username=await get_username_by_user_id(ui_2), is_admin=True)

    users_id: list[int] = await db.get_all_users_id()
    for user_id in users_id:
        if await db.is_user_admin(user_id):

            keyboard = admin_main_keyboard
        else:
            keyboard = generate_file_keyboard

        try:
            await bot.send_message(chat_id=user_id, text=BASE_MESSAGE, reply_markup=keyboard)
        except TelegramBadRequest:
            pass
