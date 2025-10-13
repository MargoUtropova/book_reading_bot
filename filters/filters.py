from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

# проверяет, является ли колбэк закладкой
class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()

# проверяет, является ли колбэк закладкой и надо ли ее удалить
class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback:CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()
