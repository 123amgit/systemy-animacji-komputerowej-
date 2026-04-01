
Laboratorium 02 – Zegar Analogowy (HTML5 Canvas)
1. Temat ćwiczenia

Implementacja zegara analogowego z wykorzystaniem technologii HTML5 Canvas oraz JavaScript (ES6), z zastosowaniem transformacji układu współrzędnych i animacji w czasie rzeczywistym.

2. Cel ćwiczenia

Celem laboratorium było:

poznanie transformacji Canvas (translate, rotate)
zrozumienie działania stosu macierzy (save, restore)
implementacja animacji przy użyciu requestAnimationFrame
zastosowanie programowania obiektowego w JavaScript
przejście od obliczeń trygonometrycznych do transformacji układu współrzędnych
3. Opis działania programu

Program rysuje zegar analogowy na elemencie <canvas>.

Zegar:

pobiera aktualny czas systemowy
przelicza go na kąty dla wskazówek
rysuje tarczę oraz wskazówki
odświeża obraz w każdej klatce animacji

W projekcie zastosowano podejście obiektowe:

klasa Clock zarządza logiką zegara
klasa Hand odpowiada za rysowanie wskazówek
4. Struktura projektu
index.html – zawiera element canvas i uruchamia skrypt
script.js – implementacja logiki zegara i animacji
README.md – dokumentacja projektu
5. Kluczowe elementy implementacji
5.1 Transformacje układu współrzędnych
środek układu przeniesiony do środka canvasa
wskazówki rysowane pionowo
obrót realizowany przez rotate()
5.2 Stos macierzy
save() przed transformacją
restore() po rysowaniu wskazówki
brak wpływu jednej transformacji na kolejne
5.3 Obliczanie czasu
sekundy uwzględniają milisekundy
minuty i godziny zależą od poprzednich jednostek
5.4 Animacja
wykorzystanie requestAnimationFrame()
płynne odświeżanie obrazu
6. Interakcja użytkownika
klawisz SPACJA zatrzymuje animację
ponowne naciśnięcie wznawia działanie zegara
7. Spełnione wymagania
✔ poprawne wyświetlanie czasu
✔ wykorzystanie klas (OOP)
✔ użycie transformacji Canvas
✔ zastosowanie save/restore
✔ płynna animacja
✔ obsługa interakcji (pauza)
✔ narysowana tarcza zegara
8. Uruchomienie programu
Otworzyć plik index.html w przeglądarce
Program uruchamia się automatycznie
9. Wnioski

Zastosowanie transformacji układu współrzędnych znacząco upraszcza rysowanie obiektów obrotowych.
Programowanie obiektowe pozwala na czytelne rozdzielenie logiki i łatwiejsze zarządzanie kodem.
requestAnimationFrame zapewnia płynną i wydajną animację.
