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

    # Funkcja zwracająca nazwe bilioteki
    def get_nazwa_na_mape(self):
        return self.nazwa_bilioteki

    # Funkcja zwraca wsporzedne X danej biblioteki
    def get_deg_x(self):
        return self.deg_x

    # Funkcja zwraca wsporzedne Y danej biblioteki
    def get_deg_y(self):
        return self.deg_y

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

    # Wyswietlanie danych obiektu
    def toString(self):
        return f"{self.nazwa_bilioteki} ; {self.location}"


class Klienci:
    # Wszystkie obiekty danej klasy
    lista_obiektow = list()

    def __init__(self, name, surname, location, biblioteka):
        self.name = name
        self.surname = surname
        self.location = location
        self.biblioteka = biblioteka
        self.deg_x, self.deg_y = get_wspolrzedne(location)

    # Funkcja zwraca imie i nazwisko klienta
    def get_nazwa_na_mape(self):
        return f'{self.name} {self.surname}'

        # Funkcja zwraca nazwe bilioteki do której dany klient jest przypisany.

    def get_biblioteka(self):
        return self.biblioteka

        # Funkcja zwraca wsporzedne X danego klienta.

    def get_deg_x(self):
        return self.deg_x

        # Funkcja zwraca wsporzedne Y danego klienta.

    def get_deg_y(self):
        return self.deg_y

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

    # Wyświetlanie danych obiektu
    def toString(self):
        return f"{self.name} {self.surname} ; {self.location} ; {self.biblioteka}"


class Pracownicy:
    # Wszystkie obiekty danej klasy
    lista_obiektow = list()

    def __init__(self, name, surname, location, biblioteka):
        self.name = name
        self.surname = surname
        self.location = location
        self.biblioteka = biblioteka
        self.deg_x, self.deg_y = get_wspolrzedne(location)

    # Funkcja zwraca imie i nazwisko pracownika

    def get_nazwa_na_mape(self):
        return f'{self.name} {self.surname}'

        # Funkcja zwraca nazwe bilioteki do ktorek dany pracownik jest przypisany.

    def get_biblioteka(self):
        return self.biblioteka

        # Funkcja zwraca wsporzedne X danego praconwika.

    def get_deg_x(self):
        return self.deg_x

    # Funkcja zwraca wsporzedne Y danego praconwika.

    def get_deg_y(self):
        return self.deg_y

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

    # Wysiwtlenie danych obiektu
    def toString(self):
        return f"{self.name} {self.surname} ; {self.location} ; {self.biblioteka}"