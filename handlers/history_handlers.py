from telebot.types import CallbackQuery

from database.common.models import db
from database.utils import CRUD
from keyboards.inline.history_kb import keyboard_for_history
from keyboards.inline.hotels_kb import keyboard_for_hotels
from loader import bot


def history(call: CallbackQuery):
    """Выводит клавиатуру с историей"""
    with db:
        user_history = CRUD.get_history_elements(db=db, telegram_id=call.from_user.id)
    bot.edit_message_text(f'История ваших запросов',
                          call.message.chat.id, call.message.message_id,
                          reply_markup=keyboard_for_history(prefix='history_item', user_history=user_history))


@bot.callback_query_handler(func=lambda call: call.data.startswith('history_item'))
def get_history(call: CallbackQuery) -> None:
    """Выводит клавиатуру с результатами выбранного ранее элемента истории"""
    with db:
        history_item = CRUD.get_history_content(db=db, history_element=call.data.lstrip('history_item'))
    with bot.retrieve_data(call.from_user.id) as data:
        data['results'] = results = history_item
    bot.edit_message_text(f'Это было найдено ранее',
                          call.message.chat.id, call.message.message_id,
                          reply_markup=keyboard_for_hotels(hotels=results, prefix='hotel'))
