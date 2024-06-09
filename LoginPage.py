# Dana klasa odpowiada za wyswietlanie okienka logowania i za zalogowanie uzytkownika

from tkinter import ttk
from tkinter import *


class LoginPage:

    def __init__(self):
        self.nazwa_uzytkownika = None  # Zmienna do przechowywania nazwy zalogowanego uzytkownika

        # Lista (a raczej słownik) użytkowników proogramu. Składa się ona z klucza jako login i wartości jako hasło.
        self.lista_uzytkownikow = {
            "admin": "admin",
            "ola": "ola",
            "michal": "michal"
        }

        # Widok okna
        self.root = Tk() #tworzenie nowego okna głównego aplikacji GUI
        self.root.resizable(False, False)
        self.root.title("Moja biblioteka - Warszawa")
        self.root.geometry("400x180")
        self.root.columnconfigure(0, weight=1, pad=0)
        self.root.columnconfigure(1, weight=1, pad=0)
        label_tytul1 = Label(self.root, text="Witamy w systemie Bibliotek Warszawa!")
        label_tytul2 = Label(self.root, text="Podaj proszę dane:")
        label_1 = Label(self.root, text="Login: ")
        label_2 = Label(self.root, text="Haslo: ")
        self.entry_login = Entry(self.root)
        self.entry_pass = Entry(self.root, show="*")
        button_login = Button(self.root, text="Zaloguj", width=17, command=self.login)
        self.label_3 = Label(self.root, text="")

        label_tytul1.grid(row=0, column=0)
        label_tytul2.grid(row=1, column=0)
        label_1.grid(row=2, column=0)
        label_2.grid(row=3, column=0)
        self.entry_login.grid(row=2, column=1)
        self.entry_pass.grid(row=3, column=1)
        button_login.grid(row=4, column=1)
        self.label_3.grid(row=5, column=0)

    # Funkcja po wcisnieciu przycisku logowania
    def login(self):
        # W danej części programu jest sprawdzne czy podany użytkownik znajduje się na liście oraz czy podane haslo jest prawidłowe.
        if self.entry_login.get() in self.lista_uzytkownikow and \
                self.lista_uzytkownikow[self.entry_login.get()] == self.entry_pass.get():
            self.nazwa_uzytkownika = self.entry_login.get()  # Ustaw nazwę zalogowanego użytkownika
            self.root.destroy()  # Zamknij dane okno
        else:
            self.label_3.config(text="Bledny login lub haslo")
