from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Reply-клавиатуры (обычные кнопки)
main_admin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_admin.add(
    KeyboardButton("Каталог"),
    KeyboardButton("Корзина"),
    KeyboardButton("Контакты"),
    KeyboardButton("Сотрудники"),
    KeyboardButton("Админ-панель"),
    KeyboardButton("Назад")
)

main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main.add(
    KeyboardButton("Каталог"),
    KeyboardButton("Корзина"),
    KeyboardButton("Контакты"),
    KeyboardButton("Сотрудники"),
    KeyboardButton("Назад")
)

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
admin_panel.add(
    KeyboardButton("Добавить товар"),
    KeyboardButton("Удалить товар"),
    KeyboardButton("Обновить товар"),
    KeyboardButton("Назад")
)

# Inline-клавиатуры (кнопки в сообщении)
catalog_list = InlineKeyboardMarkup(row_width=1)
catalog_list.add(
    InlineKeyboardButton("Видеокарты", callback_data="videocards"),
    InlineKeyboardButton("Процессоры", callback_data="processors"),
    InlineKeyboardButton("Материнские платы", callback_data="motherboards")
)

clear_cart = InlineKeyboardMarkup(row_width=2)
clear_cart.add(
    InlineKeyboardButton("Очистить корзину", callback_data="clear_all_cart"),
    InlineKeyboardButton("Удалить товар", callback_data="select_items_to_delete")
)

update_item_keyboard = InlineKeyboardMarkup(row_width=2)
update_item_keyboard.add(
    InlineKeyboardButton("Название", callback_data="update_name"),  # ✅
    InlineKeyboardButton("Описание", callback_data="update_desc"),
    InlineKeyboardButton("Цена", callback_data="update_price"),
    InlineKeyboardButton("Фото", callback_data="update_photo"),
    InlineKeyboardButton("Бренд", callback_data="update_brand")
)