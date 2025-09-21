// Blog page JS extracted from template to satisfy CSP
// Uses window.cspNonce if creating any dynamic style/script elements (none here by default)

(function() {
  'use strict';

  // Utility: debounce for search input
  function debounce(fn, wait) {
    let t;
    return function(...args) {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), wait);
    };
  }

  // Elements
  const searchInput = document.querySelector('[data-blog-search-input]');
  const postsContainer = document.querySelector('[data-blog-posts]');
  const emptyState = document.querySelector('[data-empty-state]');
  const categoryFilters = document.querySelectorAll('[data-category]');

  // Helpers
  function setActiveCategory(cat) {
    categoryFilters.forEach(el => {
      const isActive = el.getAttribute('data-category') === cat;
      el.classList.toggle('active', isActive);
      if (isActive) {
        el.setAttribute('aria-current', 'true');
      } else {
        el.removeAttribute('aria-current');
      }
    });
  }

  function renderPosts(posts) {
    if (!postsContainer) return;

    if (!Array.isArray(posts) || posts.length === 0) {
      postsContainer.innerHTML = '';
      if (emptyState) emptyState.hidden = false;
      return;
    }

    if (emptyState) emptyState.hidden = true;

    const html = posts.map(p => {
      const esc = (s) => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
      return `
        <article class="blog-card">
          <div class="blog-image">
            ${p.imageUrl ? `<img src="${esc(p.imageUrl)}" alt="${esc(p.imageAlt || p.title || 'Blog image')}" loading="lazy">` : ''}
          </div>
          <div class="blog-content">
            <div class="blog-meta">
              <span class="blog-category">${esc(p.category || 'General')}</span>
              <time class="blog-date" datetime="${esc(p.isoDate || '')}">${esc(p.date || '')}</time>
            </div>
            <h3 class="blog-title">${esc(p.title || '')}</h3>
            <p class="blog-excerpt">${esc(p.excerpt || '')}</p>
            <div class="blog-footer">
              <span class="blog-author">${esc(p.author || '')}</span>
              ${p.url ? `<a class="blog-link" href="${esc(p.url)}">Read more →</a>` : ''}
            </div>
          </div>
        </article>`;
    }).join('');

    postsContainer.innerHTML = html;
  }

  // Fetch posts function
  async function fetchPosts({ q = '', category = '' } = {}) {
    try {
      const params = new URLSearchParams();
      if (q) params.set('q', q);
      if (category) params.set('category', category);

      const res = await fetch(`/marketing/api/blog/search?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        },
        credentials: 'same-origin'
      });

      if (!res.ok) throw new Error(`Search failed: ${res.status}`);
      const data = await res.json();
      renderPosts(data.posts || []);
    } catch (err) {
      console.error('Blog search error', err);
      renderPosts([]);
    }
  }

  // Wire up search input
  if (searchInput) {
    const onSearch = debounce(() => {
      const q = searchInput.value.trim();
      const active = document.querySelector('.category-filter.active');
      const category = active ? active.getAttribute('data-category') : '';
      fetchPosts({ q, category });
    }, 250);

    searchInput.addEventListener('input', onSearch);
  }

  // Wire up category filters
  if (categoryFilters && categoryFilters.length) {
    categoryFilters.forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const category = el.getAttribute('data-category') || '';
        setActiveCategory(category);
        const q = searchInput ? searchInput.value.trim() : '';
        fetchPosts({ q, category });
      });
    });
  }

  // Initial load
  fetchPosts({});
})();
