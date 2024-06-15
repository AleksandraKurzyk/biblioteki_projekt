# Dana klasa odpowiada za wyswietlenie okienka z mapą i innymi informacjami

from tkinter import ttk  # Import w celu dodania combo boxa/pola wyboru
from tkinter import *  # Import zpaewniający elementy graficzne
from geopy.geocoders import Nominatim  # Import biblioteki ktory umożliwia pobieranie danych geograficznych
import tkintermapview  # Import do mapy

from PopUpMenu import PopUpMenu  # Import menu edycji i dodawania objektow
from Biblioteka import Biblioteki, Klienci, Pracownicy  # Import klas biznesowych

# Ustawiamy wersje agenta/komunikatora w celu podłączenia się do bazdy danych adresów, jest to wymagane w celu udanego podłączenia
# Linia wymagane z dokumentacji biblioteki ->  https://geopy.readthedocs.io/en/stable/
geolocator = Nominatim(user_agent="PostmanRuntime/7.29.0")


# Funkcja zmieniające wspolrzedne geograficzne na adres
def get_adres_z_wspolrzednych(deg_xy):
    g = geolocator.reverse(deg_xy, timeout=10)  # Po podaniu stopni goegraficznych otrzymamy adres z bazy danych
    return g.address if g is not None else "Brak danych"  # Jeżeli otrzymamy adres z stopni gegraficznych to go zwracamy jeżeli nie otrzmamy adresu zwracamy "Brak danych"


class ApplicationPage:
    def __init__(self):
        # Zmienna do przechowywania aktualnie wyswietlanych elementow
        self.aktualna_klasa = Biblioteki

        # Blok odowiadający za GUI po zalogowaniu
        self.root = Tk()  # Utworzenie nowego okienka
        self.root.resizable(False, False)  # Zablokowanie mozliwosci zmiany rozmiaru okienka
        self.root.title("Moja biblioteka - Warszawa")  # Ustawienie tytulu okienka
        self.root.geometry("1200x800")  # Ustawienie rozmiaru okienka
        # Dodanie kolumn w celu poprawnego ustawienia przycisków/pól
        self.root.columnconfigure(0, weight=1, pad=0)  # Konfiguracja kolumny 1
        self.root.columnconfigure(1, weight=1, pad=0)  # Konfiguracja kolumny 2
        self.root.columnconfigure(2, weight=1, pad=0)  # Konfiguracja kolumny 3

        # Ramki służące do ustawienia struktury GUI
        ramka_lista_obiektow = Frame(self.root)  # Ramka dla listy obiektow
        self.ramka_szczegoly_obiektu = Frame(self.root)  # Ramka dla mapy
        ramka_wybor_wysietlania = Frame(self.root)  # Ramka dla menu wyboru aktualnych obiektow

        ramka_wybor_wysietlania.grid(row=0,
                                     column=0)  # Ustalenie położenia ramki odpowiadającej za wyświetlenie listy przycisków Bibliotek, Pracownicy, Klienci
        ramka_lista_obiektow.grid(row=0,
                                  column=1)  # Ustalenie położenia ramki odpowiadającej za wyświetlenie listy obiektów np. Bibliotek
        self.ramka_szczegoly_obiektu.grid(row=1, column=0,
                                          columnspan=3)  # Ustalenie polozenia i szerokości mapy poprzed daną ile kolumn ma zajmować

        # Wybor typu wyswietlanych elementow
        # Zadeklarowanie opisow i przyciskow
        self.label_aktalna_lista = Label(ramka_wybor_wysietlania,
                                         text="Wybór aktualnego wyswietlania: (Aktualne Biblioteki)")
        # Dodanie przycisków które po kliknięciu wywołują funckję "zmiana_listy" z przekazaniem wartości np. "Biblioteka"
        button_biblioteki = Button(ramka_wybor_wysietlania, text="Biblioteki", width=20,
                                   command=lambda: self.zmiana_listy("Biblioteki"))
        button_pracownicy = Button(ramka_wybor_wysietlania, text="Pracownicy", width=20,
                                   command=lambda: self.zmiana_listy("Pracownicy"))
        button_klienci = Button(ramka_wybor_wysietlania, text="Klienci", width=20,
                                command=lambda: self.zmiana_listy("Klienci"))
        # Ustawienie przycisków w okienku
        self.label_aktalna_lista.grid(row=0, column=0, pady=10)
        button_biblioteki.grid(row=1, column=0, pady=10)
        button_pracownicy.grid(row=2, column=0, pady=10)
        button_klienci.grid(row=3, column=0, pady=10)

        # Lista obiektów
        # Zadeklarowanie opisow i przyciskow
        label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów: ")
        self.listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=80)
        # Dodanie przycisków które po kliknięciu wywołują funckję odpowiadającą danemu przycisku np. "pokaz_szczegoly_obiektu"
        button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż na mapie",
                                        command=self.pokaz_szczegoly_obiektu)
        button_dodaj_obiekt = Button(ramka_lista_obiektow, text="Dodaj obiekt", command=self.dodaj_objekt)
        button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=self.usun_obiekt)
        button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=self.edytuj_objekt)
        # Ustawienie przycisków w okienku
        label_lista_obiektow.grid(row=0, column=0, columnspan=3)
        self.listbox_lista_obiektow.grid(row=1, column=0, columnspan=4)
        button_pokaz_szczegoly.grid(row=2, column=0)
        button_dodaj_obiekt.grid(row=2, column=1)
        button_usun_obiekt.grid(row=2, column=2)
        button_edytuj_obiekt.grid(row=2, column=3)

        # Deklaracja mapy. Sama mapa zostanie wywolana pozniej
        self.map_widget = None

        # Deklarcja filtru bibliotek. Sam filtr zostanie wyswietlony po wyborze pracownikow lub klientow
        self.ramka_filtr = None
        self.filtr_bibliotek = None

        # Funkcja służąca do pokazania na mapie zaznaczonego obiektu

    def pokaz_szczegoly_obiektu(self):
        i = self.znajdz_wybrany_obiekt()[0]  # Wskaż który element zostal zaznaczony
        # Ustaw mape na ten punkt/wpółrzędne
        self.map_widget.set_position(self.aktualna_klasa.lista_obiektow[i].get_deg_x(),
                                     self.aktualna_klasa.lista_obiektow[i].get_deg_y())
        # Przybliż widok mapy na punkcie
        self.map_widget.set_zoom(18)

        # Funkcja odpowiedzialna za wyswietlenie filtru bibliotek, wyświetla po kliknięciu w Pracownika lub klienta

    def uruchom_filtr_bibiotek(self):
        self.ramka_filtr = Frame(self.root)  # Utworzenie ramki dla filtru
        self.ramka_filtr.grid(row=0, column=2, columnspan=3)  # Ustalenie polozenia ramki w okienku
        # Utworzenie opisow dla filtru
        label_tytul = Label(self.ramka_filtr, text="Filtr Bibliotek")
        label_1 = Label(self.ramka_filtr, text="Biblioteka: ")
        # Utworzenie rozwijanego menu do wyboru interesującej nas biblioteki
        self.filtr_bibliotek = ttk.Combobox(self.ramka_filtr, state="readonly", values=["Wszystkie"], width=35)
        # Ustalenie ktory element ma byc aktualnie wybrany, domyślnie pierwszy w kolejce
        self.filtr_bibliotek.current(0)
        # Podpiecie funkcji ktora ma sie uruchomic("self.odswiez_liste_obiektow()) po zmianie zaznaczonego elementu w filtrze
        self.filtr_bibliotek.bind("<<ComboboxSelected>>", lambda _: self.odswiez_liste_obiektow())

        # Ulożenie elementów w okienku
        label_tytul.grid(row=0, column=1)
        label_1.grid(row=1, column=0)
        self.filtr_bibliotek.grid(row=1, column=2)


    # Funkcja do dodawania znaczka po nacisnieciu na mape
    def event_prawy_przycisk_na_mapie(self, deg_xy):
        PopUpMenu(self.odswiez_liste_obiektow, self.aktualna_klasa, self.aktualna_klasa.labelki_pod_dodanie_obiektu(),
                  None, {"Lokalizacja": get_adres_z_wspolrzednych(deg_xy=deg_xy)})

    # Funkcja do dodawania nowego objektu
    def dodaj_objekt(self):
        PopUpMenu(self.odswiez_liste_obiektow, self.aktualna_klasa, self.aktualna_klasa.labelki_pod_dodanie_obiektu())

    # Funkcja do edycji zaznaczonego objektu
    def edytuj_objekt(self):
        PopUpMenu(self.odswiez_liste_obiektow, self.aktualna_klasa, self.aktualna_klasa.labelki_pod_edycje_obiektu(),
                  self.znajdz_wybrany_obiekt()[1])

    # Usuwanie zaznaczonego obiektu
    def usun_obiekt(self):
        self.aktualna_klasa.lista_obiektow.pop(self.znajdz_wybrany_obiekt()[0])
        self.odswiez_liste_obiektow()

    # Zmiana między obiektami (Biblioteki, Klienci, Pracownicy)
    def zmiana_listy(self, nowa_lista):
        # Spis dostepnych klas obiektow
        spis_klas = {
            "Biblioteki": Biblioteki,
            "Pracownicy": Pracownicy,
            "Klienci": Klienci
        }
        # Zmiana klasy obiektow
        self.aktualna_klasa = spis_klas[nowa_lista]
        # Aktualizacja opisu obecnego wyboru nad przyciskami Biblioteka, Prawonicy, Klienci
        self.label_aktalna_lista.config(text=f"Wybór aktualnego wyswietlania: (Aktualne {nowa_lista})")
        # Przeladowanie wszystkich dynamicznych/zmieniających się elemetow na ekranie
        self.odswiez_liste_obiektow()

    # Funkcja odpowiada za znalezienie zaznaczonego obiektu w liście wszystkich obiektow w celu jego poprawnej edycji.
    def znajdz_wybrany_obiekt(self):
        for index, aktualny_obiekt in enumerate(self.aktualna_klasa.lista_obiektow):
            if self.listbox_lista_obiektow.get(ACTIVE) == aktualny_obiekt.toString():
                return (index, aktualny_obiekt)  # Funkcja zwraca index listy oraz znaleziony obiekt.

    # Po zaktualizowaniu danych wszystkie wyświetlane elementy sa aktualizowane/odświeżane
    def odswiez_liste_obiektow(self):
        # Jesli mapa nie zostala jeszcze zaladowana, to ją uruchom.
        self.uruchom_mape() if self.map_widget is None else ''
        # Usun wszystkie znaki na mapie
        self.map_widget.delete_all_marker()
        # Usun wszystkie obiekty na liscie obiektow
        self.listbox_lista_obiektow.delete(0, END)

        # Jesli aktualnie wyswietlane sa Biblioteki to usun filtr wyboru bibliotek
        if self.aktualna_klasa == Biblioteki and self.ramka_filtr is not None:
            self.ramka_filtr.destroy()
            self.ramka_filtr = None
        # Jesli aktualne nie sa wyswietane Biblioteki, a filtr wyboru bibliotek jest ukryty to go utworz
        elif self.aktualna_klasa != Biblioteki and self.ramka_filtr is None:
            # Zlec uruchomienie filtra.
            self.uruchom_filtr_bibiotek()
            # Wyczysc dane filtra bibliotek
            self.filtr_bibliotek.delete(0, END)
            # Utworz nowa liste filtru bibliotek
            lista_do_filtru = list(map(lambda cur_bib: cur_bib.get_nazwa_na_mape(), Biblioteki.lista_obiektow))
            lista_do_filtru.append("Wszystkie")  # Do aktualnej listy bibliotek dodaj do wyboru "Wszystkie"
            self.filtr_bibliotek.config(values=lista_do_filtru)  # Ustaw nową listę
        # Przejdz po wszystkich dostepnych obiektach danej klasy i zapamietaj pozycje danego elementu.
        for idx, aktualny_obiekt in enumerate(self.aktualna_klasa.lista_obiektow):
            # Wyswietl na mapie i dodaj do listy obiektow jesli:
            #  - teraz sa wyswietlane biblioteki,
            #  - filtr jest ustawiony na wyswietlenie wsszystkego
            #  - dany obiekt zgadza sie z filtrem
            if self.aktualna_klasa == Biblioteki or \
                    self.filtr_bibliotek.get() == "Wszystkie" or \
                    self.filtr_bibliotek.get() == aktualny_obiekt.get_biblioteka():
                # Ustaw znaczek na mapie
                self.map_widget.set_position(aktualny_obiekt.get_deg_x(),
                                             aktualny_obiekt.get_deg_y(),
                                             marker=True,
                                             text=aktualny_obiekt.get_nazwa_na_mape())
                # Dodaj do listy elementow opis danego obiektu.
                self.listbox_lista_obiektow.insert(idx, aktualny_obiekt.toString())

    def uruchom_mape(self):
        # Utworzenie i ustawienie szczegolow mapy
        self.map_widget = tkintermapview.TkinterMapView(self.ramka_szczegoly_obiektu, width=900, height=500)
        self.map_widget.set_position(52.2, 21.0)  # Ustawienie pozycji startowej/widoku początkowego mapy
        self.map_widget.set_zoom(8)  # Ustawienie początkowego przybliżenia mapy
        self.map_widget.grid(row=2, column=0, columnspan=8)  # Ustalenie położenia mapy w oknie
        # Gotowa funkcja która zostanie wyołana po kliknięciu prawym przyciskiem myszy, po kliknięciu "Dodaj nowy obiekt" zostaje uruchomiona funkcja "event_prawy_przycisk_na_mapie"
        self.map_widget.add_right_click_menu_command(label="Dodaj nowy obiekt",
                                                     command=self.event_prawy_przycisk_na_mapie,
                                                     pass_coords=True)

    # Dodanie przykladowych danych w celu lepszej prezentacji programu
    def init_data(self):
        # Do listy danej klasy dopisz nowy element.
        Biblioteki.lista_obiektow.append(
            Biblioteki("Biblioteka Główna Województwa Mazowieckiego", None, "Koszykowa 26/28, Warszawa", None))
        Biblioteki.lista_obiektow.append(
            Biblioteki("Biblioteka Publiczna Praga-Południe", None, "Jana Nowaka-Jeziorańskiego 24, Warszawa", None))
        Biblioteki.lista_obiektow.append(
            Biblioteki("Biblioteka Publiczna Środmieście", None, "Marszałkowska 9/15, Warszawa", None))

        Klienci.lista_obiektow.append(
            Klienci("Adam", "Zawadzki", "20 Zlota, Warszawa", "Biblioteka Główna Województwa Mazowieckiego"))
        Klienci.lista_obiektow.append(
            Klienci("Ela", "Dzidowska", "10 Smolna, Warszawa", "Biblioteka Publiczna Praga-Południe"))
        Klienci.lista_obiektow.append(
            Klienci("Ola", "Kurzyk", "15 Bystra, Warszawa", "Biblioteka Publiczna Środmieście"))

        Pracownicy.lista_obiektow.append(
            Pracownicy("Michal", "Babiński", "25 Chmielna, Warszawa", "Biblioteka Główna Województwa Mazowieckiego"))
        Pracownicy.lista_obiektow.append(
            Pracownicy("Tomek", "Atomek", "50 Długa, Warszawa", "Biblioteka Publiczna Praga-Południe"))
        Pracownicy.lista_obiektow.append(
            Pracownicy("Kajetan", "Nowak", "75 Krótka, Warszawa", "Biblioteka Publiczna Środmieście"))

        # Na koncu odświerz GUI.
        self.odswiez_liste_obiektow()