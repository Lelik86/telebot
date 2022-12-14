from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from api_services.hotels.get_locations import get_cities_by_query


def keyboard_for_cities(cities: get_cities_by_query, prefix=str) -> InlineKeyboardMarkup:
    """Динамическая клавиатура, создаёт кнопки для каждого найденного города"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for city in cities:
        keyboard.add(InlineKeyboardButton(city.city_name, callback_data=f"{prefix}{city.city_id}"))
    return keyboard
