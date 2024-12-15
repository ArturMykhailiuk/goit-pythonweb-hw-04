import aiofiles
import argparse
import asyncio
import os
import logging


# Створення об'єкта ArgumentParser для обробки аргументів командного рядка
parser = argparse.ArgumentParser(description="Copy files based on their extensions.")
parser.add_argument("source", type=str, help="Source folder")
parser.add_argument("destination", type=str, help="Destination folder")
args = parser.parse_args()

# Ініціалізація асинхронних шляхів для вихідної та цільової папок
source_folder = args.source
destination_folder = args.destination

# Налаштування логування помилок
logging.basicConfig(level=logging.ERROR)


async def read_folder(folder):
    """Рекурсивно читає всі файли у вихідній папці та її підпапках."""
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            await copy_file(file_path)


async def copy_file(file_path):
    """Копіює кожен файл у відповідну підпапку у цільовій папці на основі його розширення."""
    try:
        file_extension = os.path.splitext(file_path)[1][
            1:
        ]  # Отримання розширення файлу без крапки
        target_folder = os.path.join(destination_folder, file_extension)
        os.makedirs(target_folder, exist_ok=True)
        target_path = os.path.join(target_folder, os.path.basename(file_path))
        async with aiofiles.open(file_path, "rb") as src_file:
            async with aiofiles.open(target_path, "wb") as dst_file:
                await dst_file.write(await src_file.read())
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


# Запуск асинхронної функції read_folder у головному блоці
if __name__ == "__main__":
    asyncio.run(read_folder(source_folder))
