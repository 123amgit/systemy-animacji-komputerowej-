# Library Ghost

## Opis projektu

Library Ghost to autorska gra 2D tworzona w Pythonie z użyciem biblioteki Raylib. Gracz będzie sterował duchem poruszającym się po bibliotece. Celem gry będzie zbieranie zagubionych stron książek i odnoszenie ich do magicznej półki, unikając przy tym strażników oraz światła latarek.

Projekt nie jest klonem gier wykonywanych na laboratoriach. Nie jest to Space Invaders, Asteroids ani on-rails shooter. Gra będzie miała własny temat, mechanikę i strukturę rozgrywki.

## Aktualny stan projektu

Na obecnym etapie wykonano podstawowy szkielet projektu:

- utworzono folder `lab_15`,
- dodano podstawową strukturę plików,
- dodano plik `README.md`,
- dodano plik `requirements.txt`,
- uruchomiono okno gry w Raylib,
- dodano prosty ekran startowy,
- dodano podstawową maszynę stanów gry:
  - `MENU`,
  - `PLAYING`,
  - `GAME_OVER`,
  - `WIN`.

Aktualnie działa ekran startowy. Po naciśnięciu `ENTER` gra przechodzi do tymczasowego ekranu rozgrywki. W kolejnych etapach zostaną dodane właściwe mechaniki gry.

## Planowane mechaniki

W kolejnych etapach projektu zostaną dodane:

- ruch gracza,
- mapa biblioteki,
- przeszkody i kolizje,
- zbieranie zagubionych stron,
- odnoszenie stron do półki,
- strażnicy z prostą sztuczną inteligencją,
- wykrywanie gracza przez światło latarki,
- pasek energii ducha,
- ekran wygranej i przegranej,
- efekty dźwiękowe.

## Własny mechanizm

Własnym mechanizmem gry będzie tryb przezroczystości ducha. Gracz będzie mógł aktywować przezroczystość, aby przechodzić przez wybrane przeszkody. Mechanika ta będzie zużywać energię ducha, więc gracz będzie musiał decydować, kiedy warto jej użyć.

## Sterowanie

Aktualnie:

- `ENTER` - rozpoczęcie gry z menu,
- `BACKSPACE` - powrót z ekranu gry do menu,
- `ESC` - zamknięcie okna gry.

Docelowo:

- `WASD` lub strzałki - ruch ducha,
- `SPACE` - aktywacja trybu przezroczystości.

## Uruchomienie projektu

1. Otworzyć folder `lab_15` w PyCharm.
2. Zainstalować zależności:

```bash
pip install -r requirements.txt
