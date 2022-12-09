from telebot.types import Message

from keyboards.inline.main_menu_kb import main_menu_kb
from loader import bot
from database.crud import User
from states.my_states import MainStates


@bot.message_handler(commands=['start'])
def bot_start(msg: Message):
    bot.set_state(msg.from_user.id, MainStates.main_menu)
    if msg.from_user.id not in User:
        User.create(user_id=msg.from_user.id)

    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.full_name}!\nЧем я могу тебе помочь?",
                     reply_markup=main_menu_kb())

    bot.delete_message(msg.chat.id, msg.message_id)
