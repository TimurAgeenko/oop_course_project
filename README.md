# FindThatAeroplane

## Описание:

Проект "FindThatAeroplane" - это приложение для поиска информации о самолетах, находящихся в воздушном пространстве над определенной страной.

Приложение поддерживает разные функции: поиск самолета по его позывному, фильтрация списка самолетов по стране регистрации,
высоте полета, получение списка топ-N самолетов по высоте полета.

## Установка:

1. Клонируйте репозиторий
   ```
   git clone https://github.com/TimurAgeenko/course_project
   ```
   
2. Установите зависимостиЖ
   ```
   poetry install
   ```
   
## Использование:

1. Класс BaseAPIHandler является абстрактным классом и определяет общие методы и атрибуты для класса APIHandler и его наследников. Он не может быть инициирован напрямую.

2. Класс BaseJSONHandler является абстрактным классом и определяет общие методы и атрибуты для класса JSONHandler и его наследников. Он не может быть инициирован напрямую.

3. Класс APIHandler является классом для обработки API запросов. При создании никакие атрибуты передавать не требуется.
   ```
   api_handler = APIHandler()
   ```
   
4. У класса APIHandler есть метод get_aeroplanes, который используется для получения информации о самолетах, находящихся в воздухе над определенной страной.
   ```
   api_handler = APIHandler()
   
   api_handler.get_aeroplanes()
   aeroplanes = api.handler.aeroplanes
   
   print(aeroplanes[0]) 
   
   # Выведет 
   [
       "4b1812",                   // ICAO24 — уникальный идентификатор борта
       "SWR438A ",                 // Callsign — позывной рейса
       "Switzerland",              // Страна регистрации ВС
       1766166618,                 // time_position — время последнего обновления позиции
       1766166618,                 // last_contact — время последнего контакта
       -0.0168,                    // longitude — долгота (°)
       51.0888,                    // latitude — широта (°)
       4267.2,                     // baro_altitude — барометрическая высота (м)
       false,                      // on_ground — находится ли самолёт на земле
       189.7,                      // velocity — горизонтальная скорость (м/с)
       129.39,                     // true_track — курс (градусы)
       14.63,                      // vertical_rate — вертикальная скорость (м/с)
       null,                       // sensors — ID сенсоров (null = неизвестно)
       4282.44,                    // geo_altitude — геометрическая высота (м)
       "2061",                     // squawk — код ответчика (транспондера)
       false,                      // spi — специальный сигнал (emergency/priority)
       0                           // position_source — источник позиции
   ]
   ```
   
5. Класс Aeroplane представляет самолет с атрибутами: позывной, страна регистрации, скорость, высота полета.
   ```
   Чтобы создать самолет, используйте следующий код:
   aeroplane = Aeroplane("Позывной", "Страна регистрации", "Скорость", "Высота полета")
   ```
   
6. У класса Aeroplane есть класс-метод cast_to_object_list, который используется для преобразования списка с информацией о самолетах,
   получаемого из метода get_aeroplanes класса APIHandler, в список объектов класса Aeroplane.
   ```
   api_handler = APIHandler()
   aeroplanes_raw = api_handler.get_aeroplanes()
   
   aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_raw)
   
   print(aeroplanes[0].callsign) # Выведет позывной
   print(aeroplanes[0].country) # Выведет страну регистрации
   print(aeroplanes[0].velocity) # Выведет скорость
   print(aeroplanes[0].altitude) # Выведет высоту полета
   ```
   
7. У класса Aeroplane есть статический метод get_top_altitude_aeroplanes, который используется для получения топ-N самолетов по высоте полета.
   ```
   aeroplanes = [
        Aeroplane("CALLSIGN1", "COUNTRY1", 1.0, 2.0),
        Aeroplane("CALLSIGN2", "COUNTRY2", 3.0, 4.0),
        Aeroplane("CALLSIGN3", "COUNTRY3", 5.0, 6.0),
        Aeroplane("CALLSIGN4", "COUNTRY3", 7.0, 8.0),
   ]
   
   sorted_aeroplanes = Aeroplane.get_top_altitude_aeroplanes(aeroplanes, 2)
   
   print(len(sorted_aeroplanes)) # Выведет 2
   print(sorted_aeroplanes[0].callsign) # Выведет "CALLSIGN4"
   print(sorted_aeroplanes[1].callsign) # Выведет "CALLSIGN3"
   ```
   
8. У класса Aeroplane есть статический метод get_aeroplanes_by_country,
   который используется для получения списка самолетов, отфильтрованных по стране регистрации.
   ```
   aeroplanes = [
        Aeroplane("CALLSIGN1", "COUNTRY1", 1.0, 2.0),
        Aeroplane("CALLSIGN2", "COUNTRY2", 3.0, 4.0),
        Aeroplane("CALLSIGN3", "COUNTRY3", 5.0, 6.0),
        Aeroplane("CALLSIGN4", "COUNTRY3", 7.0, 8.0),
   ]
   
   sorted_aeroplanes = Aeroplane.get_aeroplanes_by_country(aeroplanes, ["COUNTRY1", "COUNTRY3"])
   
   print(len(sorted_aeroplanes)) # Выведет 3
   print(sorted_aeroplanes[0].callsign) # Выведет "CALLSIGN1"
   print(sorted_aeroplanes[1].callsign) # Выведет "CALLSIGN3"
   print(sorted_aeroplanes[2].callsign) # Выведет "CALLSIGN4"
   ```
   
9. У класса Aeroplane есть статический метод get_aeroplanes_by_altitude, который используется для фильтрации самолетов по высоте полета.
   ```
   aeroplanes = [
        Aeroplane("CALLSIGN1", "COUNTRY1", 1.0, 2.0),
        Aeroplane("CALLSIGN2", "COUNTRY2", 3.0, 4.0),
        Aeroplane("CALLSIGN3", "COUNTRY3", 5.0, 6.0),
        Aeroplane("CALLSIGN4", "COUNTRY3", 7.0, 8.0),
   ]
   
   sorted_aeroplanes = Aeroplane.get_aeroplanes_by_altitude(aeroplanes, "1-4")
   
   print(len(sorted_aeroplanes)) # Выведет 2
   print(sorted_aeroplanes[0].callsign) # Выведет "CALLSIGN1"
   print(sorted_aeroplanes[1].callsign) # Выведет "CALLSIGN2"
   ```
   
10. Класс JSONHandler является классом для работы с файлами в формате json. При создании можно указать путь к файлу,
    в который будет записываться информация, есть путь не указан, то по умолчанию будет выбран путь "../data/aeroplanes.json".
    ```
    json_handler = JSONHandler()
    ```
    
11. У класса JSONHandler есть метод get_aeroplanes_list, который используется для получения списка словарей с данными о самолетах.
    ```
    В файле aeroplanes.json лежит следующая информация:
    [
    {"callsign": "CALLSIGN",
    "country": "COUNTRY",
    "velocity": 1.0,
    "altitude": 2.0}
    ]
    
    json_handler = JSONHandler()
    data = json_handler.get_aeroplanes_list()
    
    print(data) # Выведет [{"callsign": "CALLSIGN", "country": "COUNTRY", "velocity": 1.0, "altitude": 2.0}]
    ```
    
12. У класса JSONHandler есть метод add_aeroplane, который используется для добавления информации о самолете в файл.
    ```
    json_handler = JSONHandler()
    aeroplane = Aeroplane("CALLSIGN", "COUNTRY", 1.0, 2.0)
    
    json_handler.add_aeroplane(aeroplane)
    data = json_handler.get_aeroplanes_list()
    
    print(data) # Выведет [{"callsign": "CALLSIGN", "country": "COUNTRY", "velocity": 1.0, "altitude": 2.0}]
    ```
    
13. У класса JSONHandler есть метод get_aeroplane, который используется для получения информации о самолете по его позывному.
    ```
    В файле aeroplanes.json лежит следующая информация:
    [
    {"callsign": "CALLSIGN",
    "country": "COUNTRY",
    "velocity": 1.0,
    "altitude": 2.0}
    ]
    
    json_handler = JSONHandler()
    
    aeroplane = json_handler.get_aeroplane("CALLSIGN")
    print(aeroplane) # Выведет {"callsign": "CALLSIGN", "country": "COUNTRY", "velocity": 1.0, "altitude": 2.0}
    
    aeroplane = json_handler.get_aeroplane("NOT_EXISTING_CALLSIGN")
    print(aeroplane) # Выведет "Самолет с указанным позывным отсутствует в файле."
    ```
    
14. У класса JSONHandler есть метод delete_aeroplane, который используется для удаления информации о самолете по его позывному.
    ```
    В файле aeroplanes.json лежит следующая информация:
    [
    {"callsign": "CALLSIGN",
    "country": "COUNTRY",
    "velocity": 1.0,
    "altitude": 2.0}
    ]
    
    json_handler = JSONHandler()
    
    aeroplane = json_handler.delete_aeroplane("CALLSIGN")
    print(aeroplane) # Выведет "Самолет с указанным позывным успешно удален из файла."
    
    aeroplane = json_handler.delete_aeroplane("NOT_EXISTING_CALLSIGN")
    print(aeroplane) # Выведет "Самолет с указанным позывным отсутствует в файле."
    ```
    
## Тестирование:

## Тестирование

Для запуска тестов выполните следующие шаги:

1. Убедитесь, что у вас установлен `pytest`
2. В терминале наберите `pytest`, чтобы запустить тестирование
3. Проверьте результаты в консоли

При тестировании используются юнит-тесты, их результаты выводятся в консоль.

Подробные отчеты о тестировании можно найти в директории `/htmlcov/`