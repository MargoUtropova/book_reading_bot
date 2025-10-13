from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=LEXICON.get(button, button),
                callback_data=button, # то, что мы увидим в апдейте
            ) for button in buttons
        ]
    )
    return kb_builder.as_markup() # возвр объект инлайн клавиатуры

"""
Функция принимает строки, а возвращает объект клавиатуры, где в качестве текстов на кнопках -
значения из словаря LEXICON, если соответствующие ключи есть в словаре.
А если ключа в словаре нет, то текст остаётся таким же, каким был передан в функцию.
В качестве callback_data передаются значения аргументов функции.
"""