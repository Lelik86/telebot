import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('survey', "Сбор вашей информации с целью продажи"),
    ('lowprice', "Топ самых дешёвых отелей в городе"),
    ('hiprice', "Топ самых дорогих отелей в городе"),
    ('bestdeal', "Топ самых дешёвых и находящихся ближе всего к центру отелей"),
    ('history', "История ваших запросов")
)
