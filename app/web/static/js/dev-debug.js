/*
  Dev Debug Overlay
  Lightweight in-page diagnostic panel to surface:
    - Console errors/warnings
    - window.onerror and unhandledrejection
    - Basic fetch/XMLHttpRequest activity
  Load conditionally via ?debug=1 in base.html.
*/
(function () {
  try {
    const state = { errors: [], warnings: [], requests: [] };

    function escapeHtml(s) {
      return String(s || '')
        .replace(/[&<>"']/g, function (c) {
          const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
          return map[c] || c;
        });
    }

    function now() {
      return new Date().toISOString().split('T')[1].replace('Z', '');
    }

    function createEl(tag, attrs, html) {
      const el = document.createElement(tag);
      if (attrs) Object.keys(attrs).forEach(k => el.setAttribute(k, attrs[k]));
      if (html != null) el.innerHTML = html;
      return el;
    }

    function ensureStyles() {
      if (document.getElementById('dev-debug-styles')) return;
      const css = `
        .dev-debug { position: fixed; bottom: 12px; right: 12px; z-index: 2147483647; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; }
        .dev-debug .panel { background: rgba(20,20,25,0.85); color: #f2f2f2; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,0.35); backdrop-filter: blur(8px); max-width: 420px; }
        .dev-debug .header { display: flex; align-items: center; gap: 8px; padding: 8px 10px; cursor: pointer; user-select: none; }
        .dev-debug .title { font-weight: 600; font-size: 13px; letter-spacing: .2px; }
        .dev-debug .counts { margin-left: auto; display: flex; gap: 8px; }
        .dev-debug .badge { padding: 2px 6px; border-radius: 999px; font-size: 12px; font-weight: 600; }
        .dev-debug .badge.err { background: #ff4d4f; color: #fff; }
        .dev-debug .badge.warn { background: #faad14; color: #1f1f1f; }
        .dev-debug .badge.req { background: #1677ff; color: #fff; }
        .dev-debug .body { display: none; padding: 8px 10px 10px; border-top: 1px solid rgba(255,255,255,0.12); max-height: 50vh; overflow: auto; }
        .dev-debug .row { border-left: 2px solid transparent; padding: 6px 6px 6px 8px; margin: 6px 0; background: rgba(255,255,255,0.03); border-radius: 6px; }
        .dev-debug .row.err { border-left-color: #ff4d4f; }
        .dev-debug .row.warn { border-left-color: #faad14; }
        .dev-debug .row .time { opacity: .7; font-size: 12px; margin-right: 6px; }
        .dev-debug .row .src { opacity: .9; font-size: 12px; }
        .dev-debug .row pre { white-space: pre-wrap; word-break: break-word; margin: 4px 0 0; font-size: 12px; color: #eaeaea; }
        .dev-debug .filters { display: flex; gap: 6px; padding: 0 10px 8px; }
        .dev-debug .filters button { background: rgba(255,255,255,0.08); color: #eaeaea; border: 1px solid rgba(255,255,255,0.15); padding: 4px 8px; border-radius: 6px; font-size: 12px; cursor: pointer; }
        .dev-debug .filters button.active { background: rgba(255,255,255,0.2); }
      `;
      const style = createEl('style', { id: 'dev-debug-styles' });
      style.textContent = css;
      document.head.appendChild(style);
    }

    function render() {
      ensureStyles();
      let root = document.getElementById('dev-debug-root');
      if (!root) {
        root = createEl('div', { id: 'dev-debug-root', class: 'dev-debug', role: 'complementary', 'aria-label': 'Dev debug overlay' });
        document.body.appendChild(root);
      }
      const errCount = state.errors.length;
      const warnCount = state.warnings.length;
      const reqCount = state.requests.length;

      root.innerHTML = '';
      const panel = createEl('div', { class: 'panel' });
      const header = createEl('div', { class: 'header', tabindex: '0', role: 'button', 'aria-expanded': 'false' },
        `<span class="title">Debug Console</span>
         <span class="counts">
           <span class="badge err" title="Errors">${errCount}</span>
           <span class="badge warn" title="Warnings">${warnCount}</span>
           <span class="badge req" title="Network">${reqCount}</span>
         </span>`);
      const body = createEl('div', { class: 'body' });

      const controls = createEl('div', { class: 'filters' }, `
        <button data-filter="all" class="active">All</button>
        <button data-filter="errors">Errors</button>
        <button data-filter="warnings">Warnings</button>
        <button data-filter="network">Network</button>
        <button data-action="clear">Clear</button>
      `);
      body.appendChild(controls);

      const list = createEl('div');
      function addRows(items, type) {
        items.forEach(it => {
          const row = createEl('div', { class: `row ${type}` });
          const src = it.source ? ` <span class="src">(${escapeHtml(it.source)})</span>` : '';
          const msg = escapeHtml(it.message || it.url || '');
          row.innerHTML = `<span class="time">${escapeHtml(it.time)}</span>${msg}${src}`;
          if (it.details) {
            const pre = createEl('pre');
            pre.textContent = it.details;
            row.appendChild(pre);
          }
          list.appendChild(row);
        });
      }
      addRows(state.errors, 'err');
      addRows(state.warnings, 'warn');
      addRows(state.requests, 'req');
      body.appendChild(list);

      header.addEventListener('click', () => toggle());
      header.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
      controls.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (!btn) return;
        const filter = btn.getAttribute('data-filter');
        const action = btn.getAttribute('data-action');
        if (action === 'clear') {
          state.errors.length = 0; state.warnings.length = 0; state.requests.length = 0; render(); return;
        }
        controls.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
        list.innerHTML = '';
        if (filter === 'errors') addRows(state.errors, 'err');
        else if (filter === 'warnings') addRows(state.warnings, 'warn');
        else if (filter === 'network') addRows(state.requests, 'req');
        else { addRows(state.errors, 'err'); addRows(state.warnings, 'warn'); addRows(state.requests, 'req'); }
      });

      function toggle() {
        const isOpen = body.style.display === 'block';
        body.style.display = isOpen ? 'none' : 'block';
        header.setAttribute('aria-expanded', String(!isOpen));
      }

      panel.appendChild(header);
      panel.appendChild(body);
      root.appendChild(panel);
    }

    // Hook console
    ['error', 'warn'].forEach(level => {
      const orig = console[level];
      console[level] = function (...args) {
        try {
          const msg = args.map(a => typeof a === 'string' ? a : (a && a.message) || JSON.stringify(a)).join(' ');
          const entry = { time: now(), message: msg };
          if (level === 'error') state.errors.push(entry); else state.warnings.push(entry);
          render();
        } catch {}
        return orig.apply(this, args);
      };
    });

    // window error
    window.addEventListener('error', (e) => {
      try {
        const src = (e.filename || '') + (e.lineno ? `:${e.lineno}` : '') + (e.colno ? `:${e.colno}` : '');
        state.errors.push({ time: now(), message: e.message || 'Script error', source: src });
        render();
      } catch {}
    });

    // unhandled promise rejection
    window.addEventListener('unhandledrejection', (e) => {
      try {
        const msg = (e.reason && (e.reason.stack || e.reason.message)) || String(e.reason);
        state.errors.push({ time: now(), message: 'Unhandled rejection', details: msg });
        render();
      } catch {}
    });

    // fetch
    if (window.fetch) {
      const origFetch = window.fetch;
      window.fetch = function (...args) {
        const url = typeof args[0] === 'string' ? args[0] : (args[0] && args[0].url) || '';
        const started = now();
        return origFetch.apply(this, args).then(res => {
          try { state.requests.push({ time: started, message: `fetch ${res.status}`, url }); render(); } catch {}
          return res;
        }).catch(err => {
          try { state.requests.push({ time: started, message: 'fetch error', url, details: String(err) }); render(); } catch {}
          throw err;
        });
      };
    }

    // xhr
    if (window.XMLHttpRequest) {
      const OrigXHR = window.XMLHttpRequest;
      function WrappedXHR() {
        const xhr = new OrigXHR();
        let url = '';
        const origOpen = xhr.open;
        xhr.open = function (method, u, ...rest) { url = u || ''; return origOpen.call(xhr, method, u, ...rest); };
        xhr.addEventListener('loadend', function () {
          try { state.requests.push({ time: now(), message: `xhr ${xhr.status}`, url }); render(); } catch {}
        });
        xhr.addEventListener('error', function () {
          try { state.requests.push({ time: now(), message: 'xhr error', url }); render(); } catch {}
        });
        return xhr;
      }
      window.XMLHttpRequest = WrappedXHR;
    }

    // initial render
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', render);
    } else {
      render();
    }
  } catch (e) {
    try { console.error('dev-debug overlay failed to initialize', e); } catch {}
  }
})();