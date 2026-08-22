(() => {
  'use strict';
  const nativeFetch = window.fetch.bind(window);
  let liveBasePromise = null;
  const readonlyStyle = document.createElement('style');
  readonlyStyle.textContent = `
    .public-readonly .auto-sw,
    .public-readonly #catalogManage,
    .public-readonly #uploadPresaleBtn,
    .public-readonly #clearPresaleBtn,
    .public-readonly #manageBtn,
    .public-readonly .edit-row { display:none !important; }
  `;
  document.head.appendChild(readonlyStyle);
  const isWrite = options => String((options && options.method) || 'GET').toUpperCase() !== 'GET';
  const pathOf = input => new URL(input instanceof Request ? input.url : String(input), location.href).pathname;
  const localJson = (body, status = 200) => Promise.resolve(new Response(JSON.stringify(body), {
    status, headers: {'Content-Type': 'application/json; charset=utf-8'}
  }));

  async function findLiveBase() {
    if (liveBasePromise) return liveBasePromise;
    liveBasePromise = (async () => {
      const config = await nativeFetch(`urls.json?_=${Date.now()}`, {cache: 'no-store'}).then(r => r.json());
      for (const link of config.links || []) {
        const base = String(link.url || '').replace(/\/$/, '');
        if (!base) continue;
        try {
          const controller = new AbortController();
          const timer = setTimeout(() => controller.abort(), 4500);
          const response = await nativeFetch(`${base}/api/status?publicProbe=${Date.now()}`, {
            cache: 'no-store', mode: 'cors', signal: controller.signal
          });
          clearTimeout(timer);
          if (response.ok) return base;
        } catch (_) {}
      }
      throw new Error('实时服务当前离线，已保留最近一次公开快照');
    })().catch(error => { liveBasePromise = null; throw error; });
    return liveBasePromise;
  }

  window.fetch = async (input, options = {}) => {
    const path = pathOf(input);
    if (path === '/api/auto-refresh') return localJson({ok: true, enabled: false});
    if (path.startsWith('/api/') || path.startsWith('/export') || path.startsWith('/download/')) {
      if (isWrite(options) || (input instanceof Request && input.method !== 'GET')) {
        return localJson({ok: false, error: '公开站点为只读模式，请在数据主机上操作'}, 403);
      }
      try {
        const base = await findLiveBase();
        const resolved = new URL(input instanceof Request ? input.url : String(input), location.href);
        return nativeFetch(`${base}${resolved.pathname}${resolved.search}`, options);
      } catch (error) {
        if (path === '/api/inventory-catalog') {
          const tree = await nativeFetch(`stocktree.json?_=${Date.now()}`, {cache: 'no-store'}).then(r => r.json());
          return localJson({ok: true, tree, overrides: {}});
        }
        throw error;
      }
    }
    return nativeFetch(input, options);
  };

  document.documentElement.classList.add('public-readonly');
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#catalogManage,#catalogSave,#catalogReset,#uploadPresaleBtn,#clearPresaleBtn,#manageBtn,#saveOverride,#resetOverride')
      .forEach(element => element.hidden = true);
    document.addEventListener('click', async event => {
      const link = event.target.closest('a[href^="/export"]');
      if (!link) return;
      event.preventDefault();
      try {
        const base = await findLiveBase();
        location.href = base + link.getAttribute('href');
      } catch (error) { alert(error.message); }
    });
  });
})();
