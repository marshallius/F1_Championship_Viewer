RACES = [
    {"number": 1, "name": "Australian GP", "sprint": False},
    {"number": 2, "name": "Chinese GP", "sprint": True},
    {"number": 3, "name": "Japanese GP", "sprint": False},
    {"number": 4, "name": "Bahrain GP", "sprint": False},
    {"number": 5, "name": "Saudi Arabian GP", "sprint": False},
    {"number": 6, "name": "Miami GP", "sprint": True},
    {"number": 7, "name": "Canadian GP", "sprint": True},
    {"number": 8, "name": "Monaco GP", "sprint": False},
    {"number": 9, "name": "Barcelona GP", "sprint": False},
    {"number": 10, "name": "Austrian GP", "sprint": False},
    {"number": 11, "name": "British GP", "sprint": True},
    {"number": 12, "name": "Belgian GP", "sprint": False},
    {"number": 13, "name": "Hungarian GP", "sprint": False},
    {"number": 14, "name": "Dutch GP", "sprint": True},
    {"number": 15, "name": "Italian GP", "sprint": False},
    {"number": 16, "name": "Spanish GP", "sprint": False},
    {"number": 17, "name": "Azerbaijan GP", "sprint": False},
    {"number": 18, "name": "Singapore GP", "sprint": True},
    {"number": 19, "name": "United States GP", "sprint": False},
    {"number": 20, "name": "Mexican GP", "sprint": False},
    {"number": 21, "name": "Brazilian GP", "sprint": False},
    {"number": 22, "name": "Las Vegas GP", "sprint": False},
    {"number": 23, "name": "Qatar GP", "sprint": False},
    {"number": 24, "name": "Abu Dhabi GP", "sprint": False},
]


def get_race_names():
    return [race["name"] for race in RACES]