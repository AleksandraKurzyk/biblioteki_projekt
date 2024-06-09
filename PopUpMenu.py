# Jest to klasa odpowiedziana za okno edycji i dodawania obiektu

from tkinter import ttk
from tkinter import *

from Biblioteka import Biblioteki, Klienci, Pracownicy


# Spis list ktore przyjuje dana klasa

# lista_labelek
# {
# "L - tytul": string,
# "L - opis": string,
# "L - entry 1": string,
# "L - entry 2": string,
# "L - entry 4": bool,
# "L - button": string,
# }

# wstepne_dane
# {
#    "Lokalizacja:" string
# }
class PopUpMenu:
    def __init__(self, odswiez_liste_obiektow, aktualna_klasa, lista_labelek, edytowany_obiekt=None, wstepne_dane=None):
        self.edytowany_obiekt = edytowany_obiekt  # Obiekt klasy biznesowej ktory moze byc teraz edytowany
        self.odswiez_liste_obiektow = odswiez_liste_obiektow  # Jest to przekazana funkcja ktorej wywołanie odświeży GUI
        self.aktualna_klasa = aktualna_klasa  # Zawiera informacje jakiej klasy jest ww obiekt

        self.root = Tk()  # Utworzenie nowego okienka
        self.root.resizable(False, False)  # Zablokowanie mozliwosci zmiany rozmiaru okienka
        self.root.title(lista_labelek["L - tytul"])  # Ustawienie tytulu okienka
        self.root.geometry("600x200")  # Ustawienie rozmiaru okienka
        self.root.columnconfigure(0, weight=1, pad=0)  # Konfiguracja kolumny 1
        self.root.columnconfigure(1, weight=1, pad=0)  # Konfiguracja kolumny 2

        # Formularz
        # Menu jest dynamiczne. Oznacza to że nie wyświetlamy wszystkich obiektów od razu, część z nich jest wyświetlana/pomijana dopiero po wyborze klasy np. Pracownik
        # Dzięki tej zmiennej śledzimy który wiersz w oknie został zajęty poprzez dodanie kolejnego pola np. Lokalizacja. Następne pole jesteśmy w stanie dodać poniżej poprzedniego w oknie
        # Zmienna rozpoczyna się od liczby 2 dlatego że wiersz 0 (opis) oraz 1 (np. imie) zawsze istnieje i zostały ustawione statycznie reszta pól a także ich ilość
        # jest zależna od obiektu który dodajemy
        aktualny_wiersz = 2

        # Deklaracja wszystkich pol w danym oknie
        self.entry_1 = Entry(self.root, width=50)
        self.entry_2 = Entry(self.root, width=50)
        self.entry_3 = Entry(self.root, width=50)
        self.combobox_1 = ttk.Combobox(self.root, state="readonly", values=[], width=47)

        # Dane dotyczace opisu
        label_opis = Label(self.root, text=lista_labelek["L - opis"])
        label_opis.grid(row=0, column=0)
        # Pierwsze pole dla imienia lub nazwy biblioteki
        label_1 = Label(self.root, text=lista_labelek["L - entry 1"])
        label_1.grid(row=1, column=0)
        self.entry_1.grid(row=1, column=1)

        # Jesli dana klasa wymaga nazwiska to wyswietl takie pole
        if lista_labelek["L - entry 2"]:
            label_2 = Label(self.root, text=lista_labelek["L - entry 2"])
            label_2.grid(row=aktualny_wiersz, column=0)
            self.entry_2.grid(row=aktualny_wiersz, column=1)
            aktualny_wiersz += 1  # Zwiekszamy wiersz o 1, poniewaz aktualny zostal zajety

        # Kazda klasa wymaga lokalizacji, wiec te pole jest bezwarunkowe
        label_3 = Label(self.root, text="Lokalizacja: ")
        label_3.grid(row=aktualny_wiersz, column=0)
        self.entry_3.grid(row=aktualny_wiersz, column=1)
        aktualny_wiersz += 1  # Zwiekszamy wiersz o 1, poniewaz aktualny zostal zajety

        # Jesli dana klasa wymaga wybor bibliotek to wyswietl takie pole
        if lista_labelek["L - entry 4"]:
            self.combobox_1.config(
                values=list(map(lambda cur_bib: cur_bib.get_nazwa_na_mape(), Biblioteki.lista_obiektow)))
            self.combobox_1.grid(row=aktualny_wiersz, column=1)

            self.label_4 = Label(self.root, text="Biblioteka: ")
            self.label_4.grid(row=aktualny_wiersz, column=0)

            aktualny_wiersz += 1  # Zwiekszamy wiersz o 1, poniewaz aktualny zostal zajety

        # Przycisk do zatwierdzania zmian
        button_dodaj_wpis = Button(self.root, text=lista_labelek["L - button"], command=self.zapisz_zmiany)
        button_dodaj_wpis.grid(row=aktualny_wiersz, column=1)

        # Jesli zostal dostarczony obiekt do edycji to wpisz jego dane
        if edytowany_obiekt is not None:
            dane_do_pol = edytowany_obiekt.get_entry_do_formularz()
            self.entry_1.insert(0, dane_do_pol["Entry 1"])  # imie lub nazwa biblioteki
            self.entry_3.insert(0, dane_do_pol["Entry 3"])  # Lokalizacja
            self.entry_2.insert(0, dane_do_pol[
                "Entry 2"]) if "Entry 2" in dane_do_pol else ''  # Jesli jest to wpisz nazwisko

            # Jesli jest wymagany wybor bibliotek to uzupelnij tez to pole
            if "combobox_1" in dane_do_pol:
                index_in_combobox = None  # Numer w kolejnosci ktora jest aktualnie wybrana biblioteka
                # Znajdz biblioteke o tej samej nazwie i uuzpelnij który ma numer na liście
                for cur_index, cur_bib in enumerate(Biblioteki.lista_obiektow):
                    if cur_bib.get_nazwa_na_mape() == dane_do_pol["combobox_1"]:
                        index_in_combobox = cur_index
                        break
                # Ustaw aktualnie wybrana biblioteke
                self.combobox_1.current(index_in_combobox)

        # Jesli zostaly dostarczone wstepne dane, ale obiekt nie istnieje to uzupelnij pola
        elif wstepne_dane:
            self.entry_3.insert(0, wstepne_dane["Lokalizacja"])

        self.root.mainloop()

    # Funkcja do zapisu zmian
    def zapisz_zmiany(self):
        # Dodanie nowego obiektu
        if self.edytowany_obiekt is None:
            self.aktualna_klasa.lista_obiektow.append(
                self.aktualna_klasa(self.entry_1.get(), self.entry_2.get(), self.entry_3.get(), self.combobox_1.get()))
            # Edycja istniejacego
        else:
            self.edytowany_obiekt.aktualizuj_dane(self.entry_1.get(), self.entry_2.get(), self.entry_3.get(),
                                                  self.combobox_1.get())

        # Odswierz okno glowne
        self.odswiez_liste_obiektow()
        # Zamknij dane okno
        self.root.destroy()