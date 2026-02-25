class Aeroplane:
    """Класс для представления самолета"""
    __slots__ = ("callsign", "country", "velocity", "altitude")

    def __init__(self, callsign: str, country: str, velocity: float, altitude: float):
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    def __str__(self):
        callsign_str = f"'Позывной': {self.callsign.replace(" ", "")}"
        country_str = f"'Страна регистрации': {self.country}"
        velocity_str = f"'Скорость': {self.velocity}"
        altitude_str = f"'Высота полета': {self.altitude}"

        return callsign_str + ", " + country_str + ", " + velocity_str + ", " + altitude_str

    @classmethod
    def cast_to_object_list(cls, aeroplanes: list) -> list:
        """Метод для преобразования списка данных о самолетах в список объектов класса Aeroplane"""
        for aeroplane in aeroplanes:
            if not aeroplane[13]:
                aeroplane[13] = 0
        return [
            cls(callsign=aeroplane[1], country=aeroplane[2], velocity=aeroplane[9], altitude=aeroplane[13])
            for aeroplane in aeroplanes
        ]

    @staticmethod
    def get_top_altitude_aeroplanes(aeroplanes: list, top_n: int) -> list:
        """Метод для получения топ N самолетов по высоте"""
        sorted_aeroplanes = sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)
        return sorted_aeroplanes[:top_n]

    @staticmethod
    def get_aeroplanes_by_country(aeroplanes: list, countries: list) -> list:
        """Метод для получения списка самолётов, отфильтрованных по стране регистрации"""
        return [aeroplane for aeroplane in aeroplanes if aeroplane.country in countries]

    @staticmethod
    def get_aeroplanes_by_altitude(aeroplanes: list, altitude: str) -> list:
        """Метод для получения списка самолётов, отфильтрованных по высоте,
        высота задается в виде строки, например: "10000-20000" """
        altitude_range = altitude.split("-")
        if len(altitude_range) != 2:
            raise ValueError("Высота должна быть задана в виде строки, например: '10000-20000'")

        try:
            min_altitude = float(altitude_range[0])
            max_altitude = float(altitude_range[1])
        except ValueError:
            raise ValueError("Высота должна быть задана в виде строки, например: '10000-20000'")

        return [aeroplane for aeroplane in aeroplanes if min_altitude <= aeroplane.altitude <= max_altitude]
