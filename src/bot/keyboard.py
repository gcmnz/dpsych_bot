from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📄 Сгенерировать файл", callback_data="generate_file"),
    ],
    [
        InlineKeyboardButton(text="👤 Добавить пользователя", callback_data="add_user")
    ],
    [
        InlineKeyboardButton(text="🔑 Добавить администратора", callback_data="add_admin")
    ],
    [
        InlineKeyboardButton(text="🗑️ Удалить пользователя", callback_data="delete_user")
    ],
    [
        InlineKeyboardButton(text="📥 Выгрузить базу", callback_data="load_database")
    ]
])

generate_file_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📄 Сгенерировать файл", callback_data="generate_file"),
        ]
    ]
)

generate_new_file_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📄 Сгенерировать новый файл", callback_data="generate_new_file"),
        ]
    ]
)

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back"),
        ]
    ]
)
