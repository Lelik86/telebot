import json
import random
import requests

from config_data.config import HOTELS_API_URL, RAPID_API_KEY
from exceptions import ApiException


def get_hotel_images(hotel_id: str, num_of_images: int)->list:
    """
    :param hotel_id: id отеля
    :param num_of_images: необходимое количество фотографий
    :return: список url-ов
    """
    try:
        detail = _detail_request(property_id=hotel_id)
    except ApiException:
        detail = None
    photos = _parse_hotel_images(detail=detail, num_of_images=num_of_images)
    return photos


def _detail_request(property_id: str) -> dict:
    """
    Запрос к API
    :param property_id: id отеля
    :return: ответ сервера
    """
    url = f"{HOTELS_API_URL}/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": f"{property_id}"
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers, timeout=20)
    except:
        raise ApiException('Время истекло')

    if response.status_code == requests.codes.ok:
        response = json.loads(response.text)
        # with open('detail.json', 'w') as file:
        #     file.write(json.dumps(response, indent=4, ensure_ascii=False))
        return response
    else:
        raise ApiException(f'Неправильный запрос. код: {response.status_code}')


def _parse_hotel_images(detail: dict, num_of_images: int) -> list:
    """
    :param detail: словарь с сервера
    :param num_of_images: необходимое количество фотографий
    :return: список из num_of_images СЛУЧАЙНЫХ url-ов или все имеющиеся url
    """
    result = list()
    for image in detail['data']['propertyInfo']['propertyGallery']['images']:
        result.append(image['image']['url'])
    if num_of_images <= len(result):
        return random.sample(result, num_of_images)
    else:
        return random.sample(result, len(result))

# print(get_hotel_images('795873', 7))
