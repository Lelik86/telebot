import json
from datetime import date
from typing import NamedTuple
import requests

from config_data.config import HOTELS_API_URL, RAPID_API_KEY
from exceptions import ApiException


class HotelInfo(NamedTuple):
    hotel_id: str
    hotel_name: str
    distance_from_center: float
    price: str
    reviews: str
    address: str
    star_rating: str
    images: list


def search_hotels_by_filters(region_id: str, num_of_results: int, sort: str, check_in_date: date, check_out_date: date,
                             min_price: int, max_price: int, max_distance: float) -> list[HotelInfo]:
    """
    :param region_id: id региона полученный из get_locations_by_query()
    :param num_of_results: максимальное количество отелей, которое нужно найти
    :param check_in_date: Дата заселения
    :param check_out_date: Дата выселения
    :param min_price: минимальная цена за ночь
    :param max_price: максимальная цена за ночь
    :param max_distance: расстояние от центра города
    :param sort: один из типов сортировки (PRICE_LOW_TO_HIGH, PRICE_HIGH_TO_LOW, BEST_DEAL)
    :return: Возвращает список именованных кортежей HotelInfo отсортированных одним из 3 способов
    """
    hotels = _properties_request(region_id=region_id, check_in_date=check_in_date, check_out_date=check_out_date,
                                 min_price=min_price, max_price=max_price)
    if sort == 'PRICE_LOW_TO_HIGH':
        hotels = hotels[0:num_of_results]
    elif sort == 'PRICE_HIGH_TO_LOW':
        hotels = _sort_high_to_low(hotels=hotels, num_of_results=num_of_results)
    elif sort == 'BEST_DEAL':
        hotels = _sort_best_deal(hotels=hotels, max_distance=max_distance, num_of_results=num_of_results)

    results = []
    for item in hotels:
        results.append(HotelInfo(
            hotel_id=_parse_hotel_id(item),
            hotel_name=_parse_hotel_name(item),
            distance_from_center=_parse_destination(item),
            price=_parse_price(item),
            reviews=_parse_reviews(item),
            address='Не известно',
            star_rating='Не известно',
            images=[]
        ))
    return results


def _sort_high_to_low(hotels: list[dict], num_of_results: int) -> list[dict]:
    """
    Сортировка результатов по убыванию цены
    :param hotels: JSON с сервера
    :param num_of_results: необходимое количество результатов
    :return: список словарей с информацией об отелях
    """
    results = []
    for hotel in hotels[:-num_of_results - 1:-1]:
        results.append(hotel)
    return results


def _sort_best_deal(hotels: list[dict], num_of_results: int, max_distance: float) -> list[dict]:
    """
    Сортировка результатов по возрастанию цены и удалённости от центра
    :param hotels: JSON с сервера
    :param num_of_results: необходимое количество результатов
    :param max_distance: максимальная дистанция от центра
    :return: список словарей с информацией об отелях
    """
    results = []
    for hotel in hotels:
        if max_distance >= _parse_destination(hotel):
            results.append(hotel)
    results = sorted(results, key=lambda val: val['destinationInfo']['distanceFromDestination']['value'])
    results = results[0:num_of_results]
    return results


def _properties_request(region_id: str, check_in_date: date, check_out_date: date, min_price: int, max_price: int,
                        num_of_results: int = 200) -> list[dict]:
    """
    Ищет отели по множеству фильтров
    :param region_id: id региона полученный из get_locations_by_query()
    :param num_of_results: максимальное количество отелей, которое нужно найти
    :param check_in_date: Дата заселения
    :param check_out_date: Дата выселения
    :param min_price: минимальная цена за ночь
    :param max_price: максимальная цена за ночь
    :return: список словарей с информацией об отелях
    """

    url = f"{HOTELS_API_URL}/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": {
            "day": check_in_date.day,
            "month": check_in_date.month,
            "year": check_in_date.year
        },
        "checkOutDate": {
            "day": check_out_date.day,
            "month": check_out_date.month,
            "year": check_out_date.year
        },
        "rooms": [
            {
                "adults": 1,
                "children": []
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": num_of_results,
        "sort": 'PRICE_LOW_TO_HIGH',
        "filters": {"price": {
            "max": max_price,
            "min": min_price
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.request("POST", url, json=payload, headers=headers, timeout=20)
    except requests.ConnectTimeout:
        raise ApiException(ApiException.timeout_error)

    if response.status_code == requests.codes.ok:
        response = json.loads(response.text)
        try:
            properties = response['data']['propertySearch']['properties']
            return properties
        except TypeError:
            raise ApiException(ApiException.no_result)
    else:
        raise ApiException(f'{ApiException.bad_request} код: {response.status_code}')


def _parse_hotel_id(hotel: dict) -> str:
    """
    :param hotel: словарь с информацией об отеле
    :return: id отеля
    """
    hotel_id = hotel['id']
    return hotel_id


def _parse_hotel_name(hotel: dict) -> str:
    """
    :param hotel: словарь с информацией об отеле
    :return: название отеля
    """
    hotel_name = hotel['name']
    return hotel_name


def _parse_destination(hotel: dict) -> float:
    """
    :param hotel: словарь с информацией об отеле
    :return: дистанция от центра города
    """
    distance_from_center = hotel['destinationInfo']['distanceFromDestination']['value']
    return float(distance_from_center)


def _parse_price(hotel: dict) -> str:
    """
    :param hotel: словарь с информацией об отеле
    :return: стоимость проживания
    """
    price = hotel['price']['lead']['formatted']
    return price


def _parse_reviews(hotel: dict) -> str:
    """
    :param hotel: словарь с информацией об отеле
    :return: рейтинг отеля
    """
    reviews = hotel['reviews']['score']
    return reviews
