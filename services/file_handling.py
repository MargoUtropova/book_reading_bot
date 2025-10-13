# функция преобразования текста книги в словарь

import logging
import os
# import re

logger = logging.getLogger(__name__)


# def _get_part_text(text: str, start: int, size: int):
#     pattern = r'[a-zA-Zа-яА-ЯёЁ][.,!?:;](?=[a-zA-Zа-яА-ЯёЁ\s]|$)'
#     part = text[start:start + size]
#     matches = list(re.finditer(pattern, part))
#     if matches:
#         end = matches[-1].end()
#     page = part[:end]
#     return page, len(page)

# Функция, возвращающая строку с текстом страницы и её размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    # вспомогательная функция, поэтому начинается с _
    punctuation =',.!:;?'
    text = text + '\n'
    idx = max(text[:start+size].rfind(i) for i in punctuation) # нашли индекс последнего вхождения
    if (text[idx+1] or text[idx-1]) in punctuation: # проверяем соседние символы на предмет пунктуации
        size = idx - start # уменьшаем размер текста, чтобы искать точки дальше
        return _get_part_text(text, start, size)
    else:
        page_text = text[start:idx+1]
        page_size = len(page_text)
        return page_text, page_size


# Функция, формирующая словарь книги
def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    # page_size: int = 1050 - это кол-во знаков, которые помещаются на 1 стр смартфона
    try:
        with open(file=os.path.normpath(path), mode="r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        logger.error("Error reading a book: %s", e)
        raise e
    book, page, start = {}, 1, 0
    while start < len(text):
        page_text, end = _get_part_text(text, start, page_size)
        if page_text:
            book[page] = page_text.lstrip()
            start += end
            page += 1
        else:
            break

    return book
