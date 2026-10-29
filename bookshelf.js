(() => {
  const library = document.getElementById('wood-library');
  if (!library) return;
  const books = Array.from(library.querySelectorAll('.book-spine'));
  const detail = document.getElementById('book-selection');
  const title = document.getElementById('selected-title');
  const author = document.getElementById('selected-author');
  const count = document.getElementById('selected-count');
  const reader = document.getElementById('selected-reader');
  function select(book) {
    books.forEach(item => item.classList.toggle('is-selected', item === book));
    title.textContent = book.dataset.title;
    author.textContent = book.dataset.author;
    count.textContent = `${book.dataset.count} ${book.dataset.count === '1' ? 'bok' : 'bøker'} i wikien`;
    reader.href = book.href;
    detail.hidden = false;
  }
  books.forEach(book => {
    book.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      select(book);
      detail.scrollIntoView({block: 'nearest', behavior: 'auto'});
    });
  });
  let lastWidth = -1;
  function arrange() {
    const width = library.clientWidth;
    if (!width || width === lastWidth) return;
    lastWidth = width;
    const active = document.activeElement;
    const rowStyle = getComputedStyle(library.querySelector('.wood-row'));
    const usable = width - parseFloat(rowStyle.paddingLeft) - parseFloat(rowStyle.paddingRight);
    const gap = parseFloat(rowStyle.columnGap);
    const rows = document.createDocumentFragment();
    let row, used = 0;
    books.forEach(book => {
      const bookWidth = book.getBoundingClientRect().width;
      if (!row || used + gap + bookWidth > usable) {
        row = document.createElement('div');
        row.className = 'wood-row';
        rows.append(row);
        used = 0;
      }
      used += (used ? gap : 0) + bookWidth;
      row.append(book);
    });
    library.replaceChildren(rows);
    if (books.includes(active)) active.focus({preventScroll: true});
  }
  arrange();
  if ('ResizeObserver' in window) new ResizeObserver(arrange).observe(library);
  else window.addEventListener('resize', arrange);
  if (books.length) select(books[0]);
})();
