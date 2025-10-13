from aiogram.types import Message
from aiogram import Router


other_router = Router()

# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@other_router.message()
async def send_answer(message:Message) -> None:
    await message.answer(f"Извините, но я не понимаю команду {message.text}.\n"
                    "Пожалуйста, попробуйте еще раз или воспользуйтесь командой /help"
                    "для получения дополнительной информации о доступных командах")