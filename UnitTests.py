import unittest
from distance_from_mkad.models import fetch_coordinates, geodistance, nearest_distance_from_point_to_mkad


class TestCalculator(unittest.TestCase):

    def test_input_in_fetch_coordinates(self):
        self.assertEqual(fetch_coordinates('UNEXIST'), None)
        self.assertEqual(fetch_coordinates('4'), None)
        self.assertEqual(fetch_coordinates('Uhb[jdfkty'),
                         (-96.671588, 33.102797, 'Соединённые Штаты Америки, штат Техас, Коллин-Каунти, Аллен'))
        self.assertEqual(fetch_coordinates('Mytishi'),
                         (37.736743, 55.909968, 'Россия, Московская область, Мытищи'))

    def test_input_in_geodistance(self):
        self.assertEqual(geodistance(0, 0, 0, 0), 0.0)
        self.assertEqual(geodistance(0, 0, 180, 180), 0.0)
        self.assertEqual(geodistance(0, 0, 180, 0), 20015.087)
        self.assertEqual(geodistance(0, 0, 90, 0), 10007.543)
        self.assertEqual(geodistance(361, 63134, 7987, 12311), 6001.558)
        self.assertEqual(geodistance(-3619, -63134, -7987, -12311), 6457.565)
        # Расстояние от географического антипода центру Москвы до центра Москвы
        self.assertEqual(geodistance(37.617698, 55.755864, -142.382302, -55.755864), 20015.087)

    def test_input_in_nearest_distance_from_point_to_mkad(self):
        self.assertEqual(nearest_distance_from_point_to_mkad(180, 0), 12945.045)
        self.assertEqual(nearest_distance_from_point_to_mkad(37.736743, 55.909968), 2.774)  # Мытищи
        self.assertEqual(nearest_distance_from_point_to_mkad(37.617698, 55.755864), None)  # Центр Москвы
        # Расстояние от географического антипода центру Москвы до МКАДа
        self.assertEqual(nearest_distance_from_point_to_mkad(-142.382302, -55.755864), 19999.536)

        # Пограничные значения с МКАДом
        # Москва, проезд Карамзина, вл9
        self.assertEqual(nearest_distance_from_point_to_mkad(37.53729, 55.590287), None)
        # Москва, поселение Сосенское, квартал № 102, 1с1
        self.assertEqual(nearest_distance_from_point_to_mkad(37.526744, 55.589142), 0.341)
        # Москва, Алтуфьевское шоссе, 149с4
        self.assertEqual(nearest_distance_from_point_to_mkad(37.584865, 55.909781), None)
        # Москва, МКАД, 84-й километр, вл1
        self.assertEqual(nearest_distance_from_point_to_mkad(37.587146, 55.911154), 0.29)
        # Москва, МКАД, 8-й километр, 13
        self.assertEqual(nearest_distance_from_point_to_mkad(37.83138, 55.697833), 0.411)
        # Москва, МКАД, 9-й километр, 8
        self.assertEqual(nearest_distance_from_point_to_mkad(37.829566, 55.697904), None)
        # Санкт-Петербург
        self.assertEqual(nearest_distance_from_point_to_mkad(30.315644, 59.938955), 616.144)
        # Индия, штат Махараштра, Мумбаи
        self.assertEqual(nearest_distance_from_point_to_mkad(72.831711, 18.932425), 5021.981)
        # Соединённые Штаты Америки, штат Нью-Йорк, Нью-Йорк
        self.assertEqual(nearest_distance_from_point_to_mkad(-74.0028, 40.714606), 7495.855)
        # Австралия, Новый Южный Уэльс, Сидней
        self.assertEqual(nearest_distance_from_point_to_mkad(151.216484, -33.865255), 14481.852)


if __name__ == "__main__":
    unittest.main()
