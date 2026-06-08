# Lab 05 - Generator lasu w Blenderze

## Uruchomienie

1. Otwórz Blender.
2. Wejdź w `Scripting`.
3. Kliknij `Open` i wybierz `las_05.py`.
4. Kliknij `Run Script`.
5. W scenie powstanie kolekcja `Las` z podkolekcjami `Drzewa`, `Krzewy`, `Paprocie`.
6. Render zapisze się jako `las_05.png`.

## Co spełnia projekt

- słownik `TYPY_ROSLIN`,
- funkcja `stworz_rosline_typ(x, z, typ)`,
- funkcja `wybierz_typ_biomu(x, z, rozmiar_pola)`,
- funkcja `generuj_las(liczba_roslin, rozmiar_pola, seed)`,
- `random.seed(seed)` dla odtwarzalności,
- kolekcja `Las`,
- podkolekcje typów roślin,
- render `las_05.png` 1200x800.
