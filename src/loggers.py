from pathlib import Path
from src.config import dir_path
from loguru import logger

MAIN_FORMAT = "{time} | {level} | {message} | {extra}"


# Фильтер для логов
def make_filters(name):
    def filter(record):
        return record["extra"].get("filter") == name

    return filter


# region Создание директорий для логов
main_log_dir = Path(dir_path, 'logs')
main_log_dir.mkdir(parents=True, exist_ok=True)
# endregion

# region Создаёт пути для лога файлов
znak_path = main_log_dir / 'znak.log'
# endregion

# region Создание лог файлов
async def create_loggers():
    logger.add(znak_path, format=MAIN_FORMAT, filter=make_filters('znak'), enqueue=True)

# endregion

# region Переменные для логирования
znak_log = logger.bind(filter='znak')
# endregion
