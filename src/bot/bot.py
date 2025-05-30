import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BufferedInputFile
from aiogram.exceptions import TelegramBadRequest

from .api_token import API_TOKEN
from .keyboard import admin_main_keyboard, generate_file_keyboard, generate_new_file_keyboard, back_keyboard
from .utils import is_valid_name_en, is_valid_name_ru, is_valid_date
from .database import Database, convert_db_to_excel
from ..pdf import create_pdf

SUBSCRIBE_DAYS: int = 30
SUBSCRIBE_DAYS_FOR_ADMIN: int = 5555

BASE_MESSAGE: str = "🧠 Цифровая психология\n\n📄 Сгенерировано файлов: <strong>{}</strong>"
INPUT_NAME: str = "👤 Введите имя <strong>(латиницей)</strong>"
INPUT_DATE: str = '📅 Введите дату в формате дд.мм.гггг'
INCORRECT_NAME: str = '❌ Введено некорректное имя'
ACCOUNT_NOT_REGISTERED: str = "⚠️ Вы не зарегистрированы в системе\nУникальный идентификатор: <code>{}</code>"
SUBSCRIBE_EXTENDED_SUCCEED: str = '✅ Доступ успешно продлён до <strong>{}</strong>'
SUBSCRIBE_ENDS: str = '❌ Срок действия доступа истёк. Для продления обратитесь к администаторам\nУникальный идентификатор: <code>{}</code>'

INPUT_USER_IDENTIFER: str = '🆔 Введите уникальный идентификатор пользователя'
INCORRECT_IDENTIFER: str = '❌ Введён некорректный идентификатор'
U_ARE_NOT_ADMIN: str = '🔒 Не достаточно прав для выполнения данного действия'
USER_ADD_SUCCEED: str = '✅ Пользователь успешно добавлен. доступ действует до <strong>{}</strong>'
ADMIN_ADD_SUCCEED: str = '✅ Администратор успешно добавлен. доступ действует до <strong>{}</strong>'
USER_ALREADY_REGISTERED: str = '⚠️ Пользователь уже зарегистрирован'
ADMIN_ALREADY_REGISTERED: str = '⚠️ Администратор уже зарегистрирован'
USER_NOT_REGISTERED: str = '❌ Пользователь не зарегистрирован'
USER_DELETE_SUCCEED: str = '✅ Пользователь успешно удалён'
WAITING_FOR_FILE_GENERATION: str = '⏳ Файл создаётся, ожидайте...'

INVALID_NAME: str = '<strong>🔐 Авторизация</strong>\n\n❌ Введено некорректное имя'
INVALID_SURNAME: str = '<strong>🔐 Авторизация</strong>\n\n❌ Введена некорректная фамилия'
INPUT_NAME_AUTH: str = '<strong>🔐 Авторизация</strong>\n\n👤 Введите имя <strong>(кириллицей)</strong>'
INPUT_SURNAME_AUTH: str = '<strong>🔐 Авторизация</strong>\n\n👤 Введите фамилию <strong>(кириллицей)</strong>'

logging.basicConfig(level=logging.INFO)

db = Database("src/bot/database/users.db")
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


entered_name: dict[int: str] = {}  # Для хранения введённых данных {user_id: name}


class Form(StatesGroup):
    main_menu = State()
    send_name = State()
    send_date_of_birth = State()

    add_user = State()
    add_admin = State()
    delete_user = State()

    input_name = State()
    input_surname = State()


@dp.message()
async def process_message(message: types.Message, state: FSMContext):
    message_text: str = message.text
    user_id: int = message.from_user.id
    current_state = await state.get_state()

    if not await db.is_user_registered(user_id):
        await message.answer(ACCOUNT_NOT_REGISTERED.format(user_id), parse_mode='HTML')
        return

    if await db.is_subscribe_ends(user_id):
        await message.answer(SUBSCRIBE_ENDS.format(user_id), parse_mode='HTML')
        return

    if not await db.is_user_has_name(user_id):
        if current_state == Form.input_name:
            if not is_valid_name_ru(message_text):
                await bot.send_message(chat_id=user_id, text=INVALID_NAME, parse_mode='HTML')
                return

            await state.set_state(Form.input_surname)
            await db.set_user_name(user_id, message_text)
            await bot.send_message(chat_id=user_id, text=INPUT_SURNAME_AUTH, parse_mode='HTML')
            return

        await state.set_state(Form.input_name)
        await bot.send_message(chat_id=user_id, text=INPUT_NAME_AUTH, parse_mode='HTML')

        return

    if not await db.is_user_has_surname(user_id):
        if current_state == Form.input_surname:
            if not is_valid_name_ru(message_text):
                await bot.send_message(chat_id=user_id, text=INVALID_SURNAME, parse_mode='HTML')
                return

            if await db.is_user_admin(user_id):
                keyboard = admin_main_keyboard
            else:
                keyboard = generate_file_keyboard

            await state.set_state(Form.main_menu)
            await db.set_user_surname(user_id, message_text)
            await bot.send_message(chat_id=user_id, text=BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=keyboard, parse_mode='HTML')
            return

        await state.set_state(Form.input_name)
        await bot.send_message(chat_id=user_id, text=INPUT_SURNAME_AUTH, parse_mode='HTML')

        return

    if current_state is None:
        current_state = Form.main_menu

    if current_state == Form.main_menu:
        if await db.is_user_admin(user_id):
            keyboard = admin_main_keyboard
        else:
            keyboard = generate_file_keyboard

        await message.answer(BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=keyboard, parse_mode='HTML')

    elif current_state == Form.send_name:
        if not is_valid_name_en(message.text):
            await message.answer(INCORRECT_NAME, reply_markup=back_keyboard, parse_mode='HTML')
            return

        entered_name[user_id] = message.text

        await message.answer(INPUT_DATE, reply_markup=back_keyboard, parse_mode='HTML')
        await state.set_state(Form.send_date_of_birth)

    elif current_state == Form.send_date_of_birth:
        if not is_valid_date(message.text):
            await message.answer(INPUT_DATE, reply_markup=back_keyboard, parse_mode='HTML')
            return

        name: str = entered_name[user_id]
        date: str = message.text
        del entered_name[user_id]

        await message.answer(WAITING_FOR_FILE_GENERATION, parse_mode='HTML')

        pdf_bytes, pdf_path = create_pdf(name=name, date_of_birth_str=date)
        pdf = BufferedInputFile(file=pdf_bytes, filename=pdf_path)

        if await db.is_user_admin(user_id):
            keyboard = admin_main_keyboard
        else:
            keyboard = generate_new_file_keyboard

        await bot.send_document(chat_id=user_id, document=pdf)
        await db.increment_generate_file(user_id)
        await bot.send_message(chat_id=user_id, text=BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=keyboard, parse_mode='HTML')

        await state.set_state(Form.main_menu)

    elif current_state == Form.add_user:
        if not await db.is_user_admin(user_id):
            await bot.send_message(chat_id=user_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard, parse_mode='HTML')
            await state.set_state(Form.main_menu)
            return

        if not await is_check_user_id_valid(message_text):
            await bot.send_message(chat_id=user_id, text=INCORRECT_IDENTIFER, reply_markup=back_keyboard, parse_mode='HTML')
            return

        userid: int = int(message_text)
        sub_ends_time: str = (datetime.now() + timedelta(days=SUBSCRIBE_DAYS)).strftime('%d.%m.%Y')

        await state.set_state(Form.main_menu)

        if await db.is_user_registered(userid):
            if await db.is_subscribe_ends(userid):
                # Просто продливаем доступ
                await db.extend_subscribe(userid, sub_ends_time)
                await bot.send_message(chat_id=user_id, text=SUBSCRIBE_EXTENDED_SUCCEED.format(sub_ends_time), reply_markup=admin_main_keyboard, parse_mode='HTML')
                await bot.send_message(chat_id=userid, text=BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=generate_file_keyboard, parse_mode='HTML')

                return

            await bot.send_message(chat_id=user_id, text=USER_ALREADY_REGISTERED, reply_markup=admin_main_keyboard, parse_mode='HTML')

            return

        # Регистрируем
        await db.register_user(tg_user_id=userid, tg_username=await get_username_by_user_id(userid), subscribe_ends_time=sub_ends_time)
        await bot.send_message(chat_id=user_id, text=USER_ADD_SUCCEED.format(sub_ends_time), reply_markup=admin_main_keyboard, parse_mode='HTML')
        await bot.send_message(chat_id=userid, text=BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=generate_file_keyboard, parse_mode='HTML')


    elif current_state == Form.add_admin:
        if not await db.is_user_admin(user_id):
            await bot.send_message(chat_id=user_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard, parse_mode='HTML')
            await state.set_state(Form.main_menu)
            return

        if not await is_check_user_id_valid(message_text):
            await bot.send_message(chat_id=user_id, text=INCORRECT_IDENTIFER, reply_markup=back_keyboard, parse_mode='HTML')
            return

        userid: int = int(message_text)

        if await db.is_user_registered(userid):
            await bot.send_message(chat_id=user_id, text=USER_ALREADY_REGISTERED, reply_markup=admin_main_keyboard, parse_mode='HTML')
            return

        sub_ends_time: str = (datetime.now() + timedelta(days=SUBSCRIBE_DAYS_FOR_ADMIN)).strftime('%d.%m.%Y')
        result: bool = await db.register_user(userid, await get_username_by_user_id(userid), is_admin=True, subscribe_ends_time=sub_ends_time)
        if result:
            text: str = ADMIN_ADD_SUCCEED.format(sub_ends_time)
        else:
            text: str = ADMIN_ALREADY_REGISTERED

        await state.set_state(Form.main_menu)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=admin_main_keyboard, parse_mode='HTML')
        await bot.send_message(chat_id=userid, text=BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=admin_main_keyboard, parse_mode='HTML')

    elif current_state == Form.delete_user:
        if not await db.is_user_admin(user_id):
            await bot.send_message(chat_id=user_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard, parse_mode='HTML')
            await state.set_state(Form.main_menu)
            return

        if not await is_check_user_id_valid(message_text):
            await bot.send_message(chat_id=user_id, text=INCORRECT_IDENTIFER, reply_markup=back_keyboard, parse_mode='HTML')
            return

        if not await db.is_user_registered(int(message_text)):
            await bot.send_message(chat_id=user_id, text=USER_NOT_REGISTERED, reply_markup=back_keyboard, parse_mode='HTML')
            return

        await db.delete_user(int(message_text))
        await bot.send_message(chat_id=user_id, text=USER_DELETE_SUCCEED, reply_markup=admin_main_keyboard, parse_mode='HTML')


@dp.callback_query(lambda c: c.data in ['generate_file', 'generate_new_file', 'back', 'add_user', 'add_admin', 'delete_user', 'load_database'])
async def process_callback_generate_file(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id: int = callback_query.from_user.id
    message_id: int = callback_query.message.message_id

    if not await db.is_user_registered(chat_id):
        await bot.send_message(chat_id=chat_id, text=ACCOUNT_NOT_REGISTERED.format(chat_id), parse_mode='HTML')
        return

    if await db.is_subscribe_ends(chat_id):
        await bot.send_message(chat_id=chat_id, text=SUBSCRIBE_ENDS.format(chat_id), parse_mode='HTML')
        return

    if not await db.is_user_has_name(chat_id):
        await state.set_state(Form.input_name)
        await bot.send_message(chat_id=chat_id, text=INPUT_NAME_AUTH, parse_mode='HTML')
        return

    if not await db.is_user_has_surname(chat_id):
        await state.set_state(Form.input_surname)
        await bot.send_message(chat_id=chat_id, text=INPUT_SURNAME_AUTH, parse_mode='HTML')
        return

    if callback_query.data == 'generate_file':
        await state.set_state(Form.send_name)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_NAME, reply_markup=back_keyboard, parse_mode='HTML')

    elif callback_query.data == 'generate_new_file':
        await state.set_state(Form.send_name)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_NAME, reply_markup=back_keyboard, parse_mode='HTML')

    elif callback_query.data == 'add_user':
        await state.set_state(Form.add_user)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_USER_IDENTIFER, reply_markup=back_keyboard, parse_mode='HTML')

    elif callback_query.data == 'add_admin':
        await state.set_state(Form.add_admin)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_USER_IDENTIFER, reply_markup=back_keyboard, parse_mode='HTML')

    elif callback_query.data == 'delete_user':
        await state.set_state(Form.delete_user)
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_USER_IDENTIFER, reply_markup=back_keyboard, parse_mode='HTML')

    elif callback_query.data == 'load_database':
        if not await db.is_user_admin(chat_id):
            await bot.send_message(chat_id=chat_id, text=U_ARE_NOT_ADMIN, reply_markup=generate_file_keyboard, parse_mode='HTML')
            return

        excel_buffer: bytes = await convert_db_to_excel(db)
        document = BufferedInputFile(file=excel_buffer, filename='users.xlsx')
        await bot.send_document(chat_id=chat_id, document=document)

        await bot.send_message(chat_id=chat_id, text=BASE_MESSAGE.format(await db.get_user_generated_files(chat_id)), reply_markup=admin_main_keyboard, parse_mode='HTML')

    elif callback_query.data == 'back':
        await process_back(state, chat_id, message_id)


async def process_back(state: FSMContext, chat_id: int, message_id: int) -> None:
    current_state = await state.get_state()

    if current_state == Form.send_date_of_birth:
        await state.set_state(Form.send_name)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=INPUT_NAME, reply_markup=back_keyboard, parse_mode='HTML')
        return

    if current_state == Form.send_name or current_state == Form.add_user or current_state == Form.add_admin or current_state == Form.delete_user:
        await state.set_state(Form.main_menu)

        if await db.is_user_admin(chat_id):
            keyboard = admin_main_keyboard
        else:
            keyboard = generate_file_keyboard

        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=BASE_MESSAGE.format(await db.get_user_generated_files(chat_id)), reply_markup=keyboard, parse_mode='HTML')
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
    # ui_1 = 6859851833
    ui_2 = 1580689542
    # await db.register_user(tg_user_id=ui_1, tg_username=f"@{await get_username_by_user_id(ui_1)}", is_admin=True)
    await db.register_user(tg_user_id=ui_2, tg_username=await get_username_by_user_id(ui_2), is_admin=True, subscribe_ends_time=(datetime.now() + timedelta(days=2)).strftime('%d.%m.%Y'))

    users_id: list[int] = await db.get_all_users_id()
    for user_id in users_id:
        if await db.is_user_admin(user_id):

            keyboard = admin_main_keyboard
        else:
            keyboard = generate_file_keyboard

        try:
            await bot.send_message(chat_id=user_id, text=BASE_MESSAGE.format(await db.get_user_generated_files(user_id)), reply_markup=keyboard, parse_mode='HTML')
        except TelegramBadRequest:
            pass
