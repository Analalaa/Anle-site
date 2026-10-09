(() => {
  const root = document.documentElement;
  const menu = document.getElementById('pg-nav');
  const menuButton = document.querySelector('.pg-menu');
  const themeButton = document.querySelector('.pg-theme');
  const zh = root.lang === 'zh';
  function syncTheme() {
    const dark = root.classList.contains('dark');
    themeButton.setAttribute('aria-label', zh ? (dark ? '切换浅色模式' : '切换深色模式') : (dark ? 'Switch to light mode' : 'Switch to dark mode'));
  }
  themeButton.addEventListener('click', () => {
    const dark = root.classList.toggle('dark');
    root.classList.toggle('light', !dark);
    root.style.colorScheme = dark ? 'dark' : 'light';
    try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (_) {}
    syncTheme();
  });
  function setMenu(open) {
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', zh ? (open ? '关闭导航' : '打开导航') : (open ? 'Close navigation' : 'Open navigation'));
  }
  menuButton.addEventListener('click', () => setMenu(!menu.classList.contains('is-open')));
  document.addEventListener('click', event => {
    if (!event.target.closest('.pg-header')) setMenu(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.classList.contains('is-open')) { setMenu(false); menuButton.focus(); }
  });
  syncTheme();
})();
