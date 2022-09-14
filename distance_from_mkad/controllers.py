from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import fetch_coordinates, nearest_distance_from_point_to_mkad

module = Blueprint('distance_from_mkad', __name__, template_folder='templates', static_folder='static')


@module.route('/', methods=["POST", "GET"])
def index():
    return render_template('distance_from_mkad/index.html')


@module.route('/result', methods=["POST"])
def result():

    address = request.form['address']

    # Если был введён текст
    if address:

        # Пробуем найти такой объект через Яндекс API геокодер
        found_result = fetch_coordinates(address)

        # Если объект нашёлся
        if found_result:

            # Берём имя найденного адреса/объекта
            found_place_name = found_result[2]

            print('Object coords:', str(found_result[1]) + ',', found_result[0])
            # Определяем минимальное расстояние от нашего объекта до МКАДа,
            # используя координаты этого объекта (долгота, широта) из found_result
            distance = nearest_distance_from_point_to_mkad(found_result[0], found_result[1])

            # Если объект находится внутри МКАДа
            if distance:

                # Отправляем эти данные в результирующий шаблон
                return render_template('distance_from_mkad/result.html',
                                       found_place_name=found_place_name,
                                       distance=distance)

            else:
                flash('Найденный объект находиться внутри МКАД', 'error')
                return render_template('distance_from_mkad/result.html',
                                       found_place_name=found_place_name)

        else:
            flash('*Такой адрес не найден', 'error')
            return redirect(url_for('.index'))

    else:
        flash('*Поле не может быть пустым', 'error')
        return redirect(url_for('.index'))
