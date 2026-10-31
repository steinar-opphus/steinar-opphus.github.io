"""Regenerate the two bookshelf views from books.json (Python standard library)."""
import json
import re
from datetime import date
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def thickness(count):
    return 'thin' if count == 1 else 'medium' if count <= 3 else 'thick'

def render():
    books = json.loads((ROOT / 'books.json').read_text())
    assert len({b['slug'] for b in books}) == len(books), 'Duplicate reader'
    for b in books:
        assert isinstance(b['bookCount'], int) and b['bookCount'] > 0
        assert b.get('spineSize', 'thin') in ('thin', 'medium', 'thick')
        assert re.fullmatch(r'[a-z0-9-]+', b['slug'])
        assert all(re.fullmatch(r'#[0-9a-fA-F]{6}', b[k]) for k in ('color', 'ink'))
        date.fromisoformat(b['added'])
    books.sort(key=lambda b: (b['added'], b['order']), reverse=True)
    def url(b): return f"https://steinar-opphus.github.io/{b['slug']}/"
    def colors(b): return f"--cloth:{b['color']};--letters:{b['ink']};--book-height:{b['height']}px"
    def cover(b):
        return f'''<a class="book" href="{url(b)}"><div class="cover" style="background:{b['color']};color:{b['ink']}"><span class="author">{e(b['author'])}</span><span class="book-title">{'<br>'.join(map(e,b['coverLines']))}</span><span class="motif" aria-hidden="true">{e(b['symbol'])}</span><span class="edition">En bokwiki</span></div><div class="book-label"><span>{e(b['title'])}</span><span aria-hidden="true">↗</span></div></a>'''
    index = (ROOT / 'index.html').read_text()
    start, end = '<!-- BOOKS:START -->', '<!-- BOOKS:END -->'
    if start not in index:
        a = index.index('<section class="shelf"')
        z = index.index('</section>', a) + len('</section>')
        index = index[:a] + start + end + index[z:]
    block = f'''<section class="shelf" id="bokwikier" aria-labelledby="books-title"><div class="wrap"><div class="section-head"><h2 id="books-title">Nytt i bokhyllen</h2><span>De fire sist tilføyde readerne.</span></div><p class="shelf-intro">Velg hvor langt du har lest inne i wikien, og utforsk personene, stedene og sammenhengene derfra.</p><div class="books">
{''.join(cover(b) for b in books[:4])}
</div><p><a class="button" href="bokhylle.html">Se hele bokhyllen <span aria-hidden="true">→</span></a></p><p class="book-note">Uoffisielle lesefølgesvenner. Bokmotivene er egen typografisk utforming, ikke originale bokomslag.</p></div></section>'''
    a = index.index(start) + len(start)
    z = index.index(end, a)
    index = index[:a] + '\n' + block + '\n' + index[z:]
    (ROOT / 'index.html').write_text(index)
    spines = []
    for b in books:
        n = b['bookCount']
        count = f"{n} {'bok' if n == 1 else 'bøker'}"
        spines.append(f'''<a class="book-spine {b.get('spineSize', thickness(n))}" style="{colors(b)}" href="{url(b)}" data-title="{e(b['title'],quote=True)}" data-author="{e(b['author'],quote=True)}" data-count="{n}" aria-label="{e(b['title'],quote=True)} av {e(b['author'],quote=True)}, {count}"><span class="spine-type"><span class="spine-title">{e(b['title'])}</span><span class="spine-author">{e(b['author'])}</span></span><span class="spine-symbol" aria-hidden="true">{e(b['symbol'])}</span></a>''')
    page = f'''<!doctype html>
<html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bokhyllen — Steinar Opphus</title><meta name="description" content="Hele samlingen av bokwikier: utforsk bøker og serier med leseposisjonen din som spoilergrense."><meta name="theme-color" content="#f5f3eb"><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="bookshelf.css"><script src="bookshelf.js" defer></script></head>
<body><a class="skip" href="#innhold">Hopp til innhold</a><div class="wrap"><header><a class="brand" href="index.html"><span class="mark" aria-hidden="true">so</span>Steinar Opphus</a><nav aria-label="Hovedmeny"><a href="index.html#prosjekter">Prosjekter</a><a href="bokhylle.html" aria-current="page">Bokhyllen</a><a href="https://github.com/steinar-opphus">GitHub ↗</a></nav></header>
<main id="innhold"><div class="detail-hero shelf-hero"><div class="breadcrumb"><a href="index.html#bokwikier">← Til forsiden</a></div><p class="eyebrow">Bøker, verdener og sammenhenger</p><h1>Bokhyllen</h1><p class="lead">Små verdener, samlet på ett sted.</p><p class="intro">Mine bokwikier, laget med Bookwiki. Velg en bok, åpne readeren og sett hvor langt du har lest.</p></div>
<div class="shelf-heading"><p>{len(books)} wikier <span aria-hidden="true">·</span> Nyeste først</p><p class="thickness-key">Smal: 1 bok <span aria-hidden="true">·</span> Middels: 2–3 <span aria-hidden="true">·</span> Bred: 4+</p></div>
<div class="wood-library" id="wood-library" aria-label="Alle bokwikier"><div class="wood-row">{''.join(spines)}</div></div>
<section class="book-selection" id="book-selection" aria-label="Valgt bok" hidden><div aria-live="polite"><p class="eyebrow" id="selected-count"></p><h2 id="selected-title"></h2><p id="selected-author"></p></div><a class="button" id="selected-reader" href="{url(books[0])}">Åpne reader <span aria-hidden="true">↗</span></a></section>
<p class="book-note">Tykkelsen viser nåværende eller planlagt omfang av wikien. Bokryggene er egen typografisk utforming, ikke originale bokomslag.</p><p class="shelf-about"><a href="bookwiki.html">Hvordan fungerer Bookwiki? →</a></p></main><footer><span>Steinar Opphus · Et verksted i stadig utvikling.</span><a href="index.html">Til forsiden ↑</a></footer></div></body></html>'''
    (ROOT / 'bokhylle.html').write_text(page)

if __name__ == '__main__':
    render()
