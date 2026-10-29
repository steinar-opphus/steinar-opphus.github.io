# steinar-opphus.github.io
Personlig prosjektside og samling av bokwikier.


## Vedlikeholde bokhyllen

Legg til eller oppdater readere i `books.json`, og kjør `python3 scripts/render_books.py`. Commit både metadata og de genererte filene `index.html` og `bokhylle.html`. GitHub Pages serverer dem direkte; ingen byggetjeneste er nødvendig.

`added` er datoen readeren først ble lagt til, og `order` avgjør rekkefølgen innenfor samme dato. Forsiden viser de fire nyeste. Ikke endre datoen ved vanlige innholdsoppdateringer. `bookCount` bestemmer ryggbredden: én bok = smal, to–tre = middels, fire eller flere = bred. `slug` er readerens URL-sti. Farger, høyde, symbol og omslagets linjedeling kan tilpasses per wiki.
