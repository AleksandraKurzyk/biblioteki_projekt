
# Dana funkcja odopowiada za uruchomienie programu i zapewnienie dostepu do aplikacji tylko zalogowanym

from LoginPage import LoginPage
from ApplicationPage import ApplicationPage


def main():
    login_page = LoginPage()  # Zaladowanie widoku logowania
    login_page.root.mainloop()  # Uruchomienie widoku logowania
    if login_page.nazwa_uzytkownika is None:  # Sprawdzenie czy po zamknieciu okna ktos poprawnie zautoryzowal dostep
        return

    application_page = ApplicationPage() # Zaladowanie widoku aplikacji
    application_page.init_data() # Zaladowanie przykladowych danych0
    application_page.root.mainloop() # Uruchomienie widoku aplikacji z mapka


# Jest to funkcja która jest uruchamiana jako pierwsza w pliku.
if __name__ == '__main__':
    main()  # Podstawowa funkcja programu.