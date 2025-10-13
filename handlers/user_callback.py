from aiogram import Router, F
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from aiogram.types import CallbackQuery

from lexicon.lexicon import LEXICON
from keyboards.pagination import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard

user_callback = Router()

@user_callback.callback_query(F.data == 'backward')
async def process_backward_press(callback:CallbackQuery, book:dict, db:dict):
    page = db['users'][callback.from_user.id]['page']
    if page == 1:
        await callback.answer('Начало книги!')
    else:
        db['users'][callback.from_user.id]['page'] -= 1
        await callback.message.edit_text(
            text= book[page-1],
            reply_markup=create_pagination_keyboard("backward", f"{page-1}/{len(book)}", "forward"),
        )
@user_callback.callback_query(F.data == 'forward')
async def process_forward_press(callback:CallbackQuery, book:dict, db:dict):
    page = db['users'][callback.from_user.id]['page']
    if page == len(book):
        await callback.answer('Конец книги!\nЧтобы посмотреть список доступных '
                                'команд - набери /help', show_alert=True)
    else:
        db['users'][callback.from_user.id]['page'] += 1
        await callback.message.edit_text(
            text= book[page+1],
            reply_markup=create_pagination_keyboard("backward", f"{page+1}/{len(book)}", "forward"),
        )

# при нажатии на номер страницы выходит номер_стр/всего_стр. надо добавить номер_стр в закладки
@user_callback.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback:CallbackQuery, db: dict):
    page = int(callback.data.split('/')[0])
    db['users'][callback.from_user.id]['bookmarks'].add(page)
    await callback.answer('Страница добавлена в закладки!')

# при нажатии на закладку приходит колбэк с номером страницы
@user_callback.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback:CallbackQuery, book: dict, db: dict):
    page = int(callback.data)
    db["users"][callback.from_user.id]["page"] = page # сделали текущей страницу, на которую перешли из закладок
    await callback.message.edit_text(
        text=book[page],
        reply_markup=create_pagination_keyboard("backward", "{}/{}".format(page, len(book)), "forward")
    )
    await callback.answer("Перешли к закладке")

# нажатие кнопки "редактировать" в списке закладок
@user_callback.callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback:CallbackQuery, book: dict, db: dict):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(*db['users'][callback.from_user.id]['bookmarks'], book=book)
    )

# нажатие на кнопку "отмена"
@user_callback.callback_query(F.data == "cancel")
async def process_cancel_press(callback:CallbackQuery, book: dict, db: dict):
    await callback.message.edit_text(LEXICON["cancel_text"])


# удаление закладки и возврат к списку закладок
@user_callback.callback_query(IsDelBookmarkCallbackData())
async def process_delete_bookmarks(callback:CallbackQuery, book: dict, db: dict):
    page = int(callback.data.rstrip('del'))
    # await callback.answer('выбрана страница {}'.format(page))
    db['users'][callback.from_user.id]['bookmarks'].remove(page)
    await callback.answer('Закладка удалена!')
    # если еще есть закладки, то выводим список снова
    if db['users'][callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(*db['users'][callback.from_user.id]['bookmarks'], book=book)
        )
    else:
        await callback.message.edit_text(
            text= LEXICON["no_bookmarks"]
        )
