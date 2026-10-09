(() => {
  const root = document.documentElement;
  const zh = root.lang === 'zh';
  const toggle = document.querySelector('.theme-toggle');
  function syncTheme() {
    const dark = root.classList.contains('dark');
    toggle.setAttribute('aria-label', zh ? (dark ? '切换浅色模式' : '切换深色模式') : (dark ? 'Switch to light mode' : 'Switch to dark mode'));
  }
  toggle.addEventListener('click', () => {
    const dark = root.classList.toggle('dark');
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (_) {}
    syncTheme();
  });
  syncTheme();
  const filters = [...document.querySelectorAll('[data-filter]')];
  if (filters.length) {
    const posts = [...document.querySelectorAll('[data-category]')];
    filters.forEach(button => button.addEventListener('click', () => {
      filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      posts.forEach(post => { post.hidden = button.dataset.filter !== 'all' && post.dataset.category !== button.dataset.filter; });
      document.querySelectorAll('.post-year').forEach(group => { group.hidden = !group.querySelector('[data-category]:not([hidden])'); });
      document.getElementById('filter-status').textContent = zh ? `显示 ${posts.filter(p => !p.hidden).length} 篇文章` : `${posts.filter(p => !p.hidden).length} posts shown`;
    }));
  }
  const dialog = document.querySelector('.lightbox');
  if (!dialog) return;
  const photos = [...document.querySelectorAll('.photo-open')];
  const fullImage = dialog.querySelector('img');
  const count = dialog.querySelector('.lightbox-count');
  const caption = dialog.querySelector('.lightbox-caption');
  const original = dialog.querySelector('.original-photo');
  let index = 0;
  let opener;
  function showPhoto(next) {
    index = (next + photos.length) % photos.length;
    const image = photos[index].querySelector('img');
    fullImage.src = image.src;
    fullImage.alt = image.alt;
    count.textContent = `${index + 1} / ${photos.length}`;
    caption.textContent = photos[index].dataset.caption || '';
    original.href = image.src;
  }
  photos.forEach((button, i) => button.addEventListener('click', () => {
    opener = button;
    showPhoto(i);
    dialog.showModal();
    document.body.classList.add('has-lightbox');
  }));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-prev]').addEventListener('click', () => showPhoto(index - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => showPhoto(index + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); showPhoto(index + (event.key === 'ArrowLeft' ? -1 : 1)); }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('has-lightbox');
    opener?.focus({ preventScroll: true });
  });
})();
