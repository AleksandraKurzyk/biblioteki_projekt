from geopy.geocoders import Nominatim

# Ustawiamy wersje agenta/komunikatora w celu podłączenia się do bazdy danych adresów, jest to wymagane w celu udanego podłączenia
# Linia wymagane z dokumentacji biblioteki ->  https://geopy.readthedocs.io/en/stable/
# Na forach internetowych zasugerowali użycie "PostmanRuntime/7.29.0"
geolocator = Nominatim(user_agent="PostmanRuntime/7.29.0")


# Funkcka odpowiadająca za wyliczenie współrzędnych na podstawie adresu
def get_wspolrzedne(lolacja):
    g = geolocator.geocode(lolacja, timeout=10)

    # jeżeli nie uda się wyliczyć współrzędnych wyświetlany jest błąd
    if g is None:
        print("Problem z pobraniem koordynatow")
        return [0, 0]
    return g.latitude, g.longitude


class Biblioteki:
    # Wszystkie obiekty danej klasy
    lista_obiektow = list()

    def __init__(self, nazwa_bilioteki, _, location, __):
        self.nazwa_bilioteki = nazwa_bilioteki
        self.location = location
        self.deg_x, self.deg_y = get_wspolrzedne(location)

    # Opisy dla menu dodawania obiektu
    def labelki_pod_dodanie_obiektu():
        return {
            "L - tytul": "Moja biblioteka - Warszawa - dodawanie biblioteki",
            "L - opis": "Dane dla nowej biblioteki",
            "L - entry 1": "Nazwa biblioteki: ",
            "L - entry 2": False,
            "L - entry 4": False,
            "L - button": "Dodaj biblioteke",
        }


class Klienci:
    # Wszystkie obiekty danej klasy
    lista_obiektow = list()

    def __init__(self, name, surname, location, biblioteka):
        self.name = name
        self.surname = surname
        self.location = location
        self.biblioteka = biblioteka
        self.deg_x, self.deg_y = get_wspolrzedne(location)

    # Opisy dla menu dodawania obiektu
    def labelki_pod_dodanie_obiektu():
        return {
            "L - tytul": "Moja biblioteka - Warszawa - dodawanie biblioteki",
            "L - opis": "Dane dla nowej biblioteki",
            "L - entry 1": "Nazwa biblioteki: ",
            "L - entry 2": False,
            "L - entry 4": False,
            "L - button": "Dodaj biblioteke",
        }


class Pracownicy:
    # Wszystkie obiekty danej klasy
    lista_obiektow = list()

    def __init__(self, name, surname, location, biblioteka):
        self.name = name
        self.surname = surname
        self.location = location
        self.biblioteka = biblioteka
        self.deg_x, self.deg_y = get_wspolrzedne(location)

    # Opisy dla menu dodawania obiektu
    def labelki_pod_dodanie_obiektu():
        return {
            "L - tytul": "Moja biblioteka - Warszawa - dodawanie biblioteki",
            "L - opis": "Dane dla nowej biblioteki",
            "L - entry 1": "Nazwa biblioteki: ",
            "L - entry 2": False,
            "L - entry 4": False,
            "L - button": "Dodaj biblioteke",
        }