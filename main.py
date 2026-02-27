from src.models import Aeroplane
from src.api import APIHandler
from src.file_handler import JSONHandler


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    api_handler = APIHandler()
    json_handler = JSONHandler()

    print("Добро пожаловать в приложение для анализа данных о самолетах!")
    print("Для начала выберете один из двух пунктов:\n")

    while True:
        print("1. Получить информацию о самолетах, находящихся в воздушном пространстве определенной страны.")
        print("2. Работать с уже имеющейся в файле информацией.")

        main_input = input("\nВведите цифру нужного пункта: ")

        if main_input == "1":
            country = input("\nВведите название страны: ")

            # Получаем информацию о самолетах
            raw_data = api_handler.get_aeroplanes(country)

            if not raw_data:
                print("Над указанной страной нет ни одного самолета.")
            else:
                # Преобразуем информацию о самолетах в список объектов класса Aeroplane
                data = Aeroplane.cast_to_object_list(raw_data)

                # Записываем информацию в файл
                json_handler.add_aeroplanes(data, country)

                print("Отлично! Информация о самолетах получена.")
                break

        elif main_input == "2":
            country = input("\nВведите название страны для поиска в файле: ")

            # Получаем весь список из файла
            raw_data = json_handler.get_aeroplanes_list()

            if not raw_data:
                print("\nВ файле отсутствует какая-либо информация.")
            else:
                filtered_data = list(filter(lambda x: x["country"] == country, raw_data))
                dates = [item["date"] for item in filtered_data]

                print(f"\nВ файле имеется {len(filtered_data)} упоминания указанной страны.")
                print("Вот список дат, когда они были сделаны:")
                print(dates)

                while True:
                    inner_input = input("\nВведите интересующую вас дату в формате 'DD-MM-YYYY HH:MM:SS': ")

                    if inner_input not in dates:
                        print("Указанной даты нет в списке.")
                    else:
                        index = dates.index(inner_input)
                        data = filtered_data[index]["aeroplanes"]

                        # Преобразуем элементы списка в объекты класса Aeroplane
                        data = [
                            Aeroplane(
                                aeroplane["callsign"],
                                aeroplane["country"],
                                aeroplane["velocity"],
                                aeroplane["altitude"]
                            )
                            for aeroplane in data
                        ]

                        print("Отлично! Информация о самолетах получена.")
                        break
                break

    while True:
        print("\nВыберите, что вы хотите сделать:\n")

        print("1. Отфильтровать самолеты по странам регистрации.")
        print("2. Получить топ-N самолетов по высоте полета.")
        print("3. Отфильтровать самолеты по высоте полета.")
        print("4. Получить информацию об определенном самолете из файла.")
        print("5. Удалить информацию об определенном самолете из файла.")
        print("6. Выход.")

        user_input = input("\nВведите цифру нужного пункта: ")

        if user_input == "1":
            inner_input = input("\nУкажите через запятую страны для фильтрации(например: Canada, Switzerland): ")
            countries = inner_input.split(", ")

            filtered_data = Aeroplane.get_aeroplanes_by_country(data, countries)

            if not filtered_data:
                print("Самолетов с указанными странами регистрации нет в списке данных.")
            else:
                converted_data = [str(aeroplane) for aeroplane in filtered_data]
                print(f"Данные отфильтрованы по указанным странам. Всего таких самолетов {len(filtered_data)}:")
                print(converted_data)

        elif user_input == "2":
            inner_input = input("\nУкажите сколько самолетов отобрать по высоте полета: ")

            top_aeroplanes_by_altitude = Aeroplane.get_top_altitude_aeroplanes(data, int(inner_input))

            converted_data = [str(aeroplane) for aeroplane in top_aeroplanes_by_altitude]

            print(converted_data)

        elif user_input == "3":
            while True:
                inner_input = input("\nУкажите высоту полета в формате '10000-20000': ")

                try:
                    filtered_data = Aeroplane.get_aeroplanes_by_altitude(data, inner_input)
                except ValueError as e:
                    print(e.args[0])
                else:
                    if not filtered_data:
                        print("В указанном диапазоне отсутствуют самолеты.")
                        break
                    else:
                        converted_data = [str(aeroplane) for aeroplane in filtered_data]
                        print(converted_data)
                        break

        elif user_input == "4":
            inner_input = input("\nУкажите позывной самолета, по которому хотите найти информацию: ")

            aeroplane = json_handler.get_aeroplane(inner_input)

            print(aeroplane)

        elif user_input == "5":
            inner_input = input("\nУкажите позывной самолета, информацию о котором хотите удалить: ")

            print(json_handler.delete_aeroplane(inner_input))

        elif user_input == "6":
            print("\nЗавершение работы программы.")
            break


if __name__ == "__main__":
    user_interaction()
