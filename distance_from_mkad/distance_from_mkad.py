from flask import Blueprint, render_template, request, redirect, url_for
import requests

distance_from_mkad = Blueprint('distance_from_mkad', __name__, template_folder='templates', static_folder='static')
apikey_for_yandex_api = '8fb54072-d844-4ae6-ae64-162fd0c901b0'


@distance_from_mkad.route('/', methods=["POST", "GET"])
def index():
    error = request.args.get('error', None)
    return render_template('distance_from_mkad/index.html', error=error)


@distance_from_mkad.route('/result', methods=["POST", "GET"])
def result():
    city = request.form['city']
    street = request.form['street']
    house = request.form['house']

    if city and street:

        address = city + ', ' + street + ' ' + house
        coordinates = fetch_coordinates(apikey_for_yandex_api, address)

        return render_template('distance_from_mkad/result.html',
                               city=city, street=street, house=house, coordinates=coordinates)

    else:
        error = '*Город и улица являются обязательными параметрами'
        return redirect(url_for('.index', error=error))


def fetch_coordinates(apikey: str, address: str):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat
