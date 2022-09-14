import requests
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Polygon, Point
from scipy.spatial import KDTree
from typing import Tuple, Optional
from .config import apikey, mkad_coords


def fetch_coordinates(address: str) -> Optional[Tuple[float, float, str]]:
    """
    Ищет указанный адрес или объект через API Яндекс.Карт и, если находит,
    возвращает координаты этого адреса/объекта в десятичных градусах (долгота, широта)
    и название этого объекта. Либо None

    :param address: Любая строка, по которой будет осуществляться поиск объекта на
     карте. Предполагается название объекта, примерный или точный адрес, либо координаты
      объекта в формате: широта, долгота
    :return: (Долгота, широта, название объекта). Если объект не найден, то None
    """

    # URL для обращения к API геокодера, без параметров
    base_url = "https://geocode-maps.yandex.ru/1.x"
    # Непосредственно сам запрос с указанными параметрами
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    # Проверка на ошибку
    response.raise_for_status()
    # Вытаскиваем в json формате то, что нашли
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    # Если ничего не нашли, то возвращаем None
    if not found_places:
        return None

    # Берём первое место среди найденных (самое релевантное)
    most_relevant = found_places[0]
    # Берём имя этого места, как оно называется в Яндекс.Картах/Яндекс API
    found_place_name = most_relevant['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    # Берём долготу и широту этого места
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")

    # Возвращаем долготу и широту в формате float и название объекта
    return float(lon), float(lat), found_place_name


def geodistance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Вычисляет расстояние по большому кругу (в км) между двумя точками на
    земле по их координатам

    :param lon1: Долгота первой точки в десятичных градусах
    :param lat1: Широта первой точки в десятичных градусах
    :param lon2: Долгота второй точки в десятичных градусах
    :param lat2: Широта второй точки в десятичных градусах
    """

    # Десятичная долгота и широта конвертируются в радианы
    rlon1, rlat1, rlon2, rlat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # Вычисляются дельты между точками
    dlon = rlon2-rlon1
    dlat = rlat2-rlat1

    # Применяется формула Хаверсина
    a = sin(dlat/2)**2 + cos(rlat1) * cos(rlat2) * sin(dlon/2)**2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # Средний радиус Земли берётся за 6371 км

    # Округление до 3-х знаков после запятой
    distance = round(distance/1000, 3)
    return distance


def nearest_distance_from_point_to_mkad(lon: float, lat: float) -> Optional[float]:
    """
    Вычисляет ближайшее расстояние от заданной координатной точки до МКАДа (в км).
    Либо возвращает None, если точка внутри МКАДа

    :param lon: Долгота в десятичных градусах
    :param lat: Широта в десятичных градусах
    """

    # Создаём полигон из всех координат МКАДа
    polygon = Polygon(mkad_coords)

    # Проверяем лежит ли наша точка внутри полигона
    if polygon.contains(Point(lon, lat)):
        return None

    # Создаём КД-древо по координатам МКАДа
    kd_tree = KDTree(mkad_coords)
    # Находим плоскостное расстояние ближайших 8и точек МКАДа к нашей точке и берём их индексы
    indexes = kd_tree.query((lon, lat), k=8)[1]

    nearest_coordinates = list()
    # Рассчитываем реальное, более точное, геодезическое расстояние между каждой
    # из 8и точек МКАДа и нашей основной точкой
    for index in indexes:
        nearest_coordinates.append(
            geodistance(mkad_coords[index][0], mkad_coords[index][1], lon, lat)
        )

    # Возвращаем ближайшее геодезическое расстояние от изначальной точки до МКАДа
    return min(nearest_coordinates)

