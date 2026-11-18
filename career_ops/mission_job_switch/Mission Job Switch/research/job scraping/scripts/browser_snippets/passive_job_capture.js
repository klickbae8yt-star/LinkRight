// ==UserScript==
// @name         Passive Job Capture
// @namespace    linkright-passive-capture
// @version      1.5
// @description  Silently detects & captures job pages as you browse. Zero bot risk — you navigate, it only reads already-loaded DOM.
// @match        *://*/*
// @exclude      *://mail.google.com/*
// @exclude      *://docs.google.com/*
// @exclude      *://drive.google.com/*
// @exclude      *://youtube.com/*
// @exclude      *://*.youtube.com/*
// @grant        GM_setValue
// @grant        GM_getValue
// @run-at       document-idle
// @noframes
// ==/UserScript==

(function () {
  'use strict';

  // ─── TUNING ────────────────────────────────────────────────────────────────

  const SCORE_THRESHOLD = 25;   // min score to treat page as a job page
  const CAPTURE_DELAY_MS = 2000; // wait after page-load before scanning (SPA settle time)

  // ─── URL PATTERNS (+20 pts each if matched) ────────────────────────────────
  // If URL strongly suggests a job detail page, skip content scan.
  const URL_PATTERNS = [
    /\/jobs\/view\//i,               // LinkedIn job detail
    /\/jobs\/[a-z0-9-]{10,}/i,       // generic job slug
    /\/job\/[a-z0-9-]{6,}/i,
    /\/career[s]?\/[a-z0-9-]{6,}/i,
    /boards\.greenhouse\.io\/.+\/jobs\/\d+/i,
    /job-boards\.greenhouse\.io\/.+\/jobs\/\d+/i,
    /jobs\.lever\.co\/.+\/[a-f0-9-]{36}/i,
    /jobs\.ashbyhq\.com\/.+\/[a-f0-9-]{36}/i,
    /myworkdayjobs\.com\/.+\/job\//i,
    /apply\.workable\.com\/.+\/j\//i,
    /smartrecruiters\.com\/.+\/job\//i,
    /jobs\.jobvite\.com/i,
    /applytojob\.com/i,
    /[?&](jid|jobId|job_id|jobID|gh_jid|lever-origin)=/i,
    /\/posting[s]?\//i,
    /\/position[s]?\//i,
    /\/opening[s]?\//i,
    /\/vacancy/i,
  ];

  // ─── CONTENT KEYWORDS (scored) ─────────────────────────────────────────────
  const KEYWORD_SCORES = [
    [30, /responsibilities/i],
    [25, /requirements/i],
    [25, /qualifications/i],
    [20, /what you.ll do/i],
    [20, /what we.re looking for/i],
    [20, /about the role/i],
    [20, /about this job/i],
    [15, /job description/i],
    [15, /apply now/i],
    [15, /apply for this (job|role|position)/i],
    [15, /minimum qualifications/i],
    [15, /preferred qualifications/i],
    [12, /nice to have/i],
    [12, /key responsibilities/i],
    [10, /years of experience/i],
    [10, /you will be/i],
    [10, /we are looking for/i],
    [10, /ideal candidate/i],
    [10, /the role/i],
    [ 8, /compensation/i],
    [ 8, /salary/i],
    [ 8, /equity/i],
    [ 5, /hybrid/i],
    [ 5, /remote.*ok/i],
  ];

  // ─── FIELDS TO EXTRACT (best-effort regex on visible text) ─────────────────
  // These run at CSV-download time, not on each capture (cheaper).
  const JUNK_SLUGS = new Set([
    'collections','results','preview','search','jobs','apply','applications',
    'view','listing','listings','details','detail','index','home','careers',
    'recommended','discover','similar','more','new','all',
  ]);

  function extractFields(rawText, url, pageTitle, h1Title) {
    const lines = rawText.split('\n').map(l => l.trim()).filter(Boolean);

    // Title priority: H1 captured at scrape time > page title > URL slug
    let title = '';
    if (h1Title && h1Title.length > 4) {
      title = h1Title.slice(0, 120);
    }
    if (!title && pageTitle) {
      // Strip portal suffixes: "Senior PM | LinkedIn" → "Senior PM"
      // Also strip trailing portal names like "| Naukri", "| Indeed", "| LinkedIn"
      const stripped = pageTitle
        .replace(/\s*[|\-–—@]\s*(linkedin|naukri|indeed|glassdoor|amazon jobs|google|wellfound|workable|greenhouse)[\s\S]*/i, '')
        .trim();
      if (stripped.length > 4) title = stripped.slice(0, 120);
    }
    if (!title) {
      // URL slug fallback — only if not junk or numeric
      const slugMatch = url.match(/\/jobs?\/(view\/)?([^/?#]+)/i)
                     || url.match(/\/job\/([^/?#]+)/i)
                     || url.match(/\/careers?\/([^/?#]+)/i)
                     || url.match(/\/opening[s]?\/([^/?#]+)/i)
                     || url.match(/\/position[s]?\/([^/?#]+)/i);
      if (slugMatch) {
        const slug = decodeURIComponent(slugMatch[slugMatch.length - 1]);
        const isNumeric = /^\d+$/.test(slug);
        const isJunk = JUNK_SLUGS.has(slug.toLowerCase());
        if (!isNumeric && !isJunk) {
          title = slug.replace(/-/g, ' ').slice(0, 100);
        }
      }
    }

    // Company: use pipe-split from page title; strip known portal names
    let company = '';
    if (pageTitle && pageTitle.includes('|')) {
      const parts = pageTitle.split('|').map(p => p.trim());
      // Find first part that isn't a known portal name
      const portalNames = /^(linkedin|naukri|indeed|glassdoor|wellfound|workatastartup|google|amazon jobs|workable|greenhouse|lever|ashby)$/i;
      for (let i = parts.length - 1; i >= 0; i--) {
        if (!portalNames.test(parts[i]) && parts[i].length > 1) {
          company = parts[i].slice(0, 80);
          break;
        }
      }
    }
    if (!company) {
      const domain = new URL(url).hostname.replace('www.', '').split('.')[0];
      company = domain.charAt(0).toUpperCase() + domain.slice(1);
    }

    // Location: look for "Location:" label or city/state patterns
    let location = '';
    for (const line of lines) {
      if (/^location[:\s]/i.test(line)) {
        location = line.replace(/^location[:\s]*/i, '').slice(0, 80);
        break;
      }
    }
    if (!location) {
      const m = rawText.match(/\b(Remote|Hybrid|Bengaluru|Bangalore|Mumbai|Delhi|Gurgaon|Hyderabad|Chennai|Pune|Dubai|Abu Dhabi|San Francisco|New York|London|Singapore)\b/i);
      if (m) location = m[0];
    }

    // WorkAtAStartup: first raw_text line is "Job Title at Company(YCBatch)$salary..."
    if (url.includes('workatastartup.com') && lines.length > 0) {
      const m = lines[0].match(/^(.+?)\s+at\s+([^($\n]+?)(?:\s*\([A-Z]\d+\))?(?:\s*[$€£₹]|\s*•|$)/);
      if (m) {
        if (!title || /^\d+$/.test(title)) title = m[1].trim().slice(0, 120);
        if (!company || company === 'Workatastartup') company = m[2].trim().slice(0, 80);
      }
    }

    return { title, company, location };
  }

  // ─── SEARCH-RESULTS EXCLUSIONS (score = 0, never capture) ────────────────
  const SEARCH_PAGE_PATTERNS = [
    /linkedin\.com\/jobs\/search\//i,
    /linkedin\.com\/jobs\/[a-z-]+\/?(?:\?(?!.*currentJobId)|$)/i, // collections/feed without a selected job
    /google\.com\/about\/careers\/applications\/jobs\/results\/\?/i, // google search results page (has ?q=)
    /naukri\.com\/(?!job-listings)[a-z0-9-]+-jobs(?:-in-[a-z-]+)?(?:[?#]|$)/i, // naukri search (not JD)
    /indeed\.com\/jobs\?/i,
    /glassdoor\.com\/Job\/jobs\.htm/i,
    /wellfound\.com\/jobs\?/i,
    /workatastartup\.com\/jobs\?/i,
  ];

  // ─── SCORE PAGE ────────────────────────────────────────────────────────────
  function scorePage() {
    const url = window.location.href;

    // Bail immediately on known search-results pages
    for (const pat of SEARCH_PAGE_PATTERNS) {
      if (pat.test(url)) return 0;
    }

    let score = 0;

    // URL scoring
    for (const pat of URL_PATTERNS) {
      if (pat.test(url)) { score += 20; break; }
    }

    // Content scoring (on visible text only, fast)
    const text = document.body ? document.body.innerText : '';
    if (!text || text.length < 200) return 0;

    for (const [pts, re] of KEYWORD_SCORES) {
      if (re.test(text)) score += pts;
      if (score >= SCORE_THRESHOLD * 2) break; // early exit
    }

    return score;
  }

  // ─── EXTRACT CLEAN TEXT ────────────────────────────────────────────────────
  function getPageText() {
    const host = window.location.hostname;

    // LinkedIn: body.innerText returns serialized JSON — use specific content selectors instead
    if (host.includes('linkedin.com')) {
      const liSelectors = [
        '.jobs-description__content',
        '.jobs-box__html-content',
        '.jobs-description-content__text',
        '#job-details',
        '.jobs-description',
        '.job-view-layout',
        '[class*="job-details"]',
      ];
      for (const sel of liSelectors) {
        const el = document.querySelector(sel);
        if (el && el.innerText && el.innerText.trim().length > 300) {
          return el.innerText.replace(/\n{3,}/g, '\n\n').trim().slice(0, 15000);
        }
      }
      return ''; // no readable job content found — capture() will discard this
    }

    // Default: clone body, strip noise
    const clone = document.body.cloneNode(true);
    for (const tag of clone.querySelectorAll(
      'script, style, noscript, nav, footer, header, ' +
      '[class*="cookie"], [class*="banner"], [class*="popup"], ' +
      '[id*="cookie"], [id*="banner"], [aria-hidden="true"]'
    )) { tag.remove(); }
    return clone.innerText.replace(/\n{3,}/g, '\n\n').trim().slice(0, 15000);
  }

  // ─── STORAGE (cross-domain via GM_setValue) ────────────────────────────────
  const STORAGE_KEY = 'passive_job_captures_v1';

  function loadCaptures() {
    try { return JSON.parse(GM_getValue(STORAGE_KEY, '[]')); } catch (_) { return []; }
  }

  function saveCaptures(arr) {
    GM_setValue(STORAGE_KEY, JSON.stringify(arr));
  }

  function clearCaptures() {
    saveCaptures([]);
  }

  // ─── CAPTURE ───────────────────────────────────────────────────────────────
  function capture() {
    const url = window.location.href;
    const captures = loadCaptures();

    // Deduplicate by URL
    if (captures.some(c => c.url === url)) return;

    const score = scorePage();
    if (score < SCORE_THRESHOLD) return;

    const rawText  = getPageText();
    // Discard if no readable content (LinkedIn selector miss, or JSON body)
    if (!rawText || rawText.length < 300 || rawText.trimStart().startsWith('{')) {
      console.log(`[PassiveJobCapture] Skipped (no readable content): ${window.location.href.slice(0, 80)}`);
      return;
    }
    const pageTitle = document.title || '';
    const portal   = window.location.hostname.replace('www.', '');
    const now      = new Date().toISOString();
    const h1El     = document.querySelector('h1');
    const h1Title  = h1El ? h1El.innerText.trim().slice(0, 150) : '';

    captures.push({ url, page_title: pageTitle, h1_title: h1Title, portal, captured_at: now, score, raw_text: rawText });
    saveCaptures(captures);

    updateBadge(captures.length);
    console.log(`[PassiveJobCapture] Captured (score=${score}): ${pageTitle.slice(0, 60)}`);
  }

  // ─── SPA NAVIGATION HOOK ───────────────────────────────────────────────────
  // LinkedIn/Wellfound/Naukri use pushState — no real page reload.
  let lastURL = location.href;

  function onURLChange() {
    if (location.href === lastURL) return;
    lastURL = location.href;
    setTimeout(capture, CAPTURE_DELAY_MS);
  }

  const origPush    = history.pushState.bind(history);
  const origReplace = history.replaceState.bind(history);

  history.pushState = function (...a) {
    origPush(...a);
    onURLChange();
  };
  history.replaceState = function (...a) {
    origReplace(...a);
    onURLChange();
  };
  window.addEventListener('popstate', onURLChange);

  // ─── FLOATING UI ────────────────────────────────────────────────────────────
  let badge, panel;

  function buildUI() {
    // Badge
    badge = document.createElement('div');
    badge.id = '__pjc_badge';
    Object.assign(badge.style, {
      position: 'fixed', bottom: '18px', right: '18px', zIndex: '2147483647',
      background: '#0a84ff', color: '#fff', fontFamily: 'system-ui, sans-serif',
      fontSize: '13px', fontWeight: '600', padding: '6px 12px',
      borderRadius: '20px', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,.3)',
      userSelect: 'none', lineHeight: '1.4',
    });
    badge.title = 'Passive Job Capture — click to manage';
    badge.addEventListener('click', (e) => { e.stopPropagation(); e.stopImmediatePropagation(); togglePanel(); });
    document.body.appendChild(badge);

    // Panel
    panel = document.createElement('div');
    panel.id = '__pjc_panel';
    Object.assign(panel.style, {
      position: 'fixed', bottom: '56px', right: '18px', zIndex: '2147483647',
      background: '#1c1c1e', color: '#f2f2f7', fontFamily: 'system-ui, sans-serif',
      fontSize: '13px', width: '340px', maxHeight: '420px',
      borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,.5)',
      overflow: 'hidden', display: 'none', flexDirection: 'column',
    });
    panel.addEventListener('click', (e) => { e.stopPropagation(); e.stopImmediatePropagation(); });
    document.body.appendChild(panel);
    updateBadge(loadCaptures().length);
  }

  function updateBadge(count) {
    if (!badge) return;
    badge.textContent = count === 0 ? '📋 0 jobs' : `📋 ${count} job${count === 1 ? '' : 's'}`;
    badge.style.background = count > 0 ? '#30d158' : '#0a84ff';
  }

  function togglePanel() {
    if (!panel) return;
    const showing = panel.style.display !== 'none';
    if (showing) { panel.style.display = 'none'; return; }
    renderPanel();
    panel.style.display = 'flex';
  }

  function renderPanel() {
    const captures = loadCaptures();
    panel.innerHTML = '';

    // Header
    const hdr = document.createElement('div');
    Object.assign(hdr.style, {
      padding: '12px 14px', borderBottom: '1px solid #3a3a3c',
      fontWeight: '700', fontSize: '14px', color: '#fff', flexShrink: '0',
    });
    hdr.textContent = `📋 ${captures.length} job page${captures.length !== 1 ? 's' : ''} captured`;
    panel.appendChild(hdr);

    // List
    const list = document.createElement('div');
    Object.assign(list.style, {
      overflowY: 'auto', flex: '1', padding: '6px 0',
    });
    if (captures.length === 0) {
      const empty = document.createElement('div');
      Object.assign(empty.style, { padding: '14px', color: '#8e8e93', textAlign: 'center' });
      empty.textContent = 'Browse job pages — they appear here automatically.';
      list.appendChild(empty);
    } else {
      captures.slice().reverse().forEach(c => {
        const item = document.createElement('div');
        Object.assign(item.style, {
          padding: '8px 14px', borderBottom: '1px solid #2c2c2e', lineHeight: '1.4',
        });
        const title = document.createElement('div');
        title.style.color = '#f2f2f7';
        title.style.fontSize = '12px';
        title.textContent = (c.page_title || c.url).slice(0, 70);
        const meta = document.createElement('div');
        meta.style.color = '#8e8e93';
        meta.style.fontSize = '11px';
        meta.textContent = `${c.portal} · score=${c.score} · ${c.captured_at.slice(0, 16).replace('T', ' ')}`;
        item.appendChild(title);
        item.appendChild(meta);
        list.appendChild(item);
      });
    }
    panel.appendChild(list);

    // Buttons
    const btns = document.createElement('div');
    Object.assign(btns.style, {
      display: 'flex', gap: '8px', padding: '10px 14px',
      borderTop: '1px solid #3a3a3c', flexShrink: '0',
    });

    const dlBtn = makeBtn('⬇ Download CSV', '#0a84ff', () => downloadCSV(captures));
    const clrBtn = makeBtn('✕ Clear', '#ff453a', () => {
      if (confirm('Clear all captured jobs?')) { clearCaptures(); renderPanel(); updateBadge(0); }
    });
    btns.appendChild(dlBtn);
    btns.appendChild(clrBtn);
    panel.appendChild(btns);
  }

  function makeBtn(label, bg, onClick) {
    const b = document.createElement('button');
    b.textContent = label;
    Object.assign(b.style, {
      flex: '1', background: bg, color: '#fff', border: 'none',
      borderRadius: '8px', padding: '8px 0', cursor: 'pointer',
      fontWeight: '600', fontSize: '13px',
    });
    b.addEventListener('click', onClick);
    return b;
  }

  // ─── CSV EXPORT ────────────────────────────────────────────────────────────
  function esc(v) {
    const s = String(v || '').replace(/"/g, '""');
    return /[",\n\r]/.test(s) ? `"${s}"` : s;
  }

  function downloadCSV(captures) {
    if (!captures.length) { alert('No jobs captured yet.'); return; }

    const cols = ['url', 'title', 'company', 'location', 'portal', 'captured_at', 'score', 'raw_text'];
    const rows = captures.map(c => {
      const { title, company, location } = extractFields(c.raw_text, c.url, c.page_title, c.h1_title || '');
      return { url: c.url, title, company, location, portal: c.portal,
               captured_at: c.captured_at, score: c.score, raw_text: c.raw_text };
    });

    const csv = [
      cols.join(','),
      ...rows.map(r => cols.map(col => esc(r[col])).join(','))
    ].join('\n');

    const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
    const a    = Object.assign(document.createElement('a'), {
      href: URL.createObjectURL(blob),
      download: `jobs_passive_${new Date().toISOString().slice(0, 10)}.csv`,
    });
    document.body.appendChild(a);
    a.click();
    a.remove();
    console.log(`[PassiveJobCapture] Exported ${rows.length} jobs to CSV`);
  }

  // ─── INIT ────────────────────────────────────────────────────────────────
  // Wait for body to be ready before injecting UI
  function init() {
    if (!document.body) { setTimeout(init, 200); return; }
    buildUI();
    // Initial capture attempt for current page
    setTimeout(capture, CAPTURE_DELAY_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
