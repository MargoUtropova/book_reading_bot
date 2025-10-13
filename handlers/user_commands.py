from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from copy import deepcopy

from keyboards.pagination import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard
from lexicon.lexicon import LEXICON

user_commands = Router()

@user_commands.message(CommandStart())
async def process_start_command(message:Message, db: dict):
    # проверка пользователя
    id = message.from_user.id
    if id not in db['users']:
        db['users'][id] = deepcopy(db['user_template'])
        db['users'][id]['page'] = 1
    await message.answer(LEXICON[message.text])

@user_commands.message(Command(commands='help'))
async def process_help_command(message:Message):
    await message.answer(LEXICON[message.text])


@user_commands.message(Command(commands=['beginning', 'continue']))
async def process_beginning_command(message:Message, book:dict, db:dict):
    id = message.from_user.id
    if 'beginning'in message.text:
        db['users'][id]['page'] = 1
    page = db['users'][id]['page']
    await message.answer(
        text= book[page],
        reply_markup=create_pagination_keyboard("backward", f"{page}/{len(book)}", "forward")
        )

@user_commands.message(Command(commands='bookmarks'))
async def process_bookmark_command(message:Message, book:dict, db:dict):
    id = message.from_user.id
    if db['users'][id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *db['users'][id]['bookmarks'], book=book
            )
        )
    else: #если у пользователя нет закладок
        await message.answer(text=LEXICON['no_bookmarks'])
