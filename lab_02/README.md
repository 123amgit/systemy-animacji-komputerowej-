# Laboratorium 02 - Zegar analogowy w HTML5 Canvas

## Temat ćwiczenia
Implementacja zegara analogowego z wykorzystaniem HTML5 Canvas oraz JavaScript ES6.

## Cel ćwiczenia
Celem laboratorium było zapoznanie się z:
- transformacjami układu współrzędnych w Canvas,
- użyciem metod `translate()`, `rotate()`, `save()` i `restore()`,
- animacją w czasie rzeczywistym za pomocą `requestAnimationFrame()`,
- zastosowaniem programowania obiektowego w JavaScript.

## Opis programu
Program wyświetla zegar analogowy na elemencie `canvas`. Tarcza zegara jest rysowana dynamicznie, a wskazówki godzinowa, minutowa i sekundowa ustawiane są zgodnie z aktualnym czasem systemowym.

Projekt został wykonany w sposób obiektowy:
- klasa `Clock` odpowiada za logikę działania zegara,
- klasa `Hand` odpowiada za rysowanie pojedynczej wskazówki.

Dodatkowo zaimplementowano możliwość zatrzymania i wznowienia animacji za pomocą klawisza **Spacja**.

## Zastosowane elementy
W projekcie wykorzystano:
- HTML5
- CSS3
- JavaScript ES6
- Canvas API

## Najważniejsze funkcjonalności
- wyświetlanie aktualnego czasu,
- płynny ruch sekundnika z uwzględnieniem milisekund,
- różne długości i grubości wskazówek,
- rysowanie tarczy zegara z podziałką minutową i godzinową,
- obsługa pauzy i wznowienia działania programu.

## Uruchomienie
Aby uruchomić projekt, należy otworzyć plik `index.html` w przeglądarce internetowej.

## Sterowanie
- `Spacja` - zatrzymanie / wznowienie animacji
