from telebot.types import Message

from loader import bot


# Команда /bestdeal
# После ввода команды у пользователя запрашивается:
# 1. Город, где будет проводиться поиск.
# 2. Диапазон цен.
# 3. Диапазон расстояния, на котором находится отель от центра.
# 4. Количество отелей, которые необходимо вывести в результате (не больше заранее определённого максимума).
# 5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
#   a. При положительном ответе пользователь также вводит количество необходимых фотографий
#   (не больше заранее определённого максимума)

@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message):
    pass
    # TODO
