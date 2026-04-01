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

## Struktura projektu
- `index.html` - plik uruchamiający projekt i zawierający element `canvas`
- `script.js` - plik zawierający logikę działania zegara
- `README.md` - opis projektu

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

## Spełnione wymagania
Projekt spełnia wymagania zadania laboratoryjnego:
- poprawne użycie klas ES6,
- rozdzielenie logiki programu,
- zastosowanie transformacji układu współrzędnych,
- użycie `save()` i `restore()`,
- animacja w czasie rzeczywistym,
- obsługa interakcji użytkownika,
- estetyczna tarcza zegara.

## Zrzut ekranu
W tym miejscu należy dodać zrzut ekranu działającego programu, np.:

```html
<img src="screenshot.png" alt="Zegar analogowy">
