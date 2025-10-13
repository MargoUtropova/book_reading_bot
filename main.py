#  импорт библиотек
import asyncio
import logging
# импорт библиотечных модулей
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# импорт из файлов проекта
from database.database import init_db
from handlers.user_commands import user_commands
from handlers.user_callback import user_callback
from handlers.other import other_router
from config.config import Config, load_config
from keyboards.menu_commands import set_main_menu
from services.file_handling import prepare_book

# инициализация логгера
logger = logging.getLogger(__name__)

# функция конфигурации и запуска бота
async def main():
    # загружаем config
    config: Config = load_config()

    # задаем базовую конфигурацию логирования
    logging.basicConfig(
        level=config.log.level,
        format=config.log.format
    )

    # выводим в консоль информацию о старте бота
    logger.info('Bot started')

    # инициализируем бот и диспетчер
    bot = Bot(
                token=config.bot.token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
              )
    dp = Dispatcher()

    # подготовка книги
    logger.info("Prepare book")
    book = prepare_book("book/book.txt")
    logger.info("The book is uploaded. Total pages: %d", len(book))

    # инициализируем БД
    db: dict = init_db()


    # Сохраняем готовую книгу и "базу данных" в `workflow_data`
    dp.workflow_data.update(book=book, db=db)

    # Настраиваем главное меню команд бота
    await set_main_menu(bot)

    # регистриуем роутеры
    dp.include_router(user_commands)
    dp.include_router(user_callback)
    dp.include_router(other_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())