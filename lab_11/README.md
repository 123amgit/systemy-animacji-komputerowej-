# Laboratorium 11 - Animacja geometrii rośliny przez bpy

## Opis

Projekt przedstawia animację rośliny wykonaną w Blenderze za pomocą skryptu Python `bpy`.

Jako źródłowy asset użyto pliku `lab08_materialy_oswietlenie.blend`, który zawiera gotową roślinę w kolekcji `Roslina_Hero`.

## Wykonane elementy

- import kolekcji `Roslina_Hero` z pliku `.blend`,
- automatyczne wyszukiwanie liści po nazwie `Roslina_Lisc`,
- animacja liści przez sinusoidalną rotację,
- animacja pąków `Roslina_Pak` przez skalowanie,
- delikatna animacja łodygi,
- zapis końcowej sceny do `roslina_ozywiona_11.blend`,
- render animacji do pliku `roslina_ozywiona_11.mp4`.

## Pliki

- `lab08_materialy_oswietlenie.blend` - źródłowy asset rośliny
- `roslina_animacja_geometrii.py` - skrypt generujący animację
- `roslina_ozywiona_11.blend` - końcowa scena z animacją
- `roslina_ozywiona_11.mp4` - wyrenderowana animacja

## Uruchomienie

1. Otworzyć `roslina_ozywiona_11.blend` w Blenderze.
2. Przejść do zakładki `Scripting`.
3. Otworzyć `roslina_animacja_geometrii.py`.
4. Uruchomić skrypt przez `Alt + P`.
5. Odtworzyć animację na timeline od klatki 1 do 125.

## Render

Animację można wyrenderować skrótem:

`Ctrl + F12`
