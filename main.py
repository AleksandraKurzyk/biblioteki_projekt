
# Dana funkcja odopowiada za uruchomienie programu i zapewnienie dostepu do aplikacji tylko zalogowanym

from LoginPage import LoginPage


def main():
    login_page = LoginPage()  # Zaladowanie widoku logowania
    login_page.root.mainloop()  # Uruchomienie widoku logowania
    if login_page.nazwa_uzytkownika is None:  # Sprawdzenie czy po zamknieciu okna ktos poprawnie zautoryzowal dostep
        return

# Jest to funkcja która jest uruchamiana jako pierwsza w pliku.
if __name__ == '__main__':
    main()  # Podstawowa funkcja programu.