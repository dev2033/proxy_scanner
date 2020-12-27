"""Конфиг для логирования"""
from loguru import logger

# serialize=True - нужен, если хотим сохранять файл с логами в json формате
logger.add(
    "logging/debug.json",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="2 MB",
    compression="zip",
    serialize=True
)
