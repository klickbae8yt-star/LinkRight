// ==UserScript==
// @name         LinkedIn Post to n8n AI Assistant
// @namespace    https://n8n.io/
// @version      1.0.0
// @description  Extracts LinkedIn post data and sends it directly to your n8n AI webhook for instant comment and outreach generation.
// @author       n8n Automation
// @match        https://www.linkedin.com/*
// @match        https://linkedin.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=n8n.io
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @connect      localhost
// @connect      *
// ==/UserScript==

(function () {
  'use strict';

  // Default n8n webhook endpoint URL
  const DEFAULT_WEBHOOK_URL = 'http://localhost:5678/webhook/linkedin-post-ingest';

  // Get or set stored webhook URL
  let webhookUrl = GM_getValue('n8n_webhook_url', DEFAULT_WEBHOOK_URL);

  const injectStyles = () => {
    if (document.getElementById('n8n-script-styles')) return;

    const style = document.createElement('style');
    style.id = 'n8n-script-styles';
    style.textContent = `
      .n8n-btn-wrapper {
        display: inline-flex;
        align-items: center;
        margin-left: 8px;
        position: relative;
      }

      .n8n-trigger-btn {
        background: linear-gradient(135deg, #FF6D5A 0%, #EA4C89 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 16px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

      .n8n-trigger-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(234, 76, 137, 0.3);
        opacity: 0.95;
      }

      .n8n-trigger-btn:disabled {
        background: #CCCCCC !important;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
      }

      .n8n-toast {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 999999;
        background: #1E293B;
        color: #F8FAFC;
        padding: 14px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 14px;
        max-width: 380px;
        border-left: 4px solid #FF6D5A;
        animation: n8nSlideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }

      @keyframes n8nSlideIn {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }

      .n8n-config-fab {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 99999;
        background: #1E293B;
        color: #FFF;
        border-radius: 50%;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        font-size: 18px;
        transition: transform 0.2s;
      }

      .n8n-config-fab:hover {
        transform: scale(1.1);
      }
    `;
    document.head.appendChild(style);
  };

  const showToast = (message, isError = false) => {
    const existing = document.querySelector('.n8n-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'n8n-toast';
    if (isError) toast.style.borderLeftColor = '#EF4444';
    toast.innerHTML = message;

    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
  };

  const extractPostData = (postElement) => {
    try {
      // 1. Author Name
      const authorNameEl = postElement.querySelector(
        '.update-components-actor__title span[aria-hidden="true"], .feed-shared-actor__title, .update-components-actor__title'
      );
      const authorName = authorNameEl ? authorNameEl.innerText.split('\n')[0].trim() : 'LinkedIn Member';

      // 2. Author Headline / Designation
      const authorHeadlineEl = postElement.querySelector(
        '.update-components-actor__description, .feed-shared-actor__description'
      );
      const authorHeadline = authorHeadlineEl ? authorHeadlineEl.innerText.trim() : '';

      // 3. Author Profile URL
      const authorLinkEl = postElement.querySelector(
        'a.update-components-actor__image-link, a.feed-shared-actor__container-link, a.update-components-actor__title-link'
      );
      let authorProfileUrl = authorLinkEl ? authorLinkEl.href : '';
      if (authorProfileUrl.includes('?')) {
        authorProfileUrl = authorProfileUrl.split('?')[0]; // Clean query parameters
      }

      // 4. Post Main Text Content
      const textEl = postElement.querySelector(
        '.update-components-text, .feed-shared-update-v2__commentary, .feed-shared-inline-show-more-text'
      );
      const postText = textEl ? textEl.innerText.trim() : '';

      // 5. External Link attached to post
      const linkEl = postElement.querySelector('.update-components-text a[href*="http"], .feed-shared-article a[href*="http"]');
      const externalLink = linkEl ? linkEl.href : null;

      // 6. Post URN / Activity ID
      const urn = postElement.getAttribute('data-urn') || postElement.getAttribute('data-activity-urn') || '';

      // 7. Reaction & Comment counts (Best effort from DOM)
      const reactionEl = postElement.querySelector('.social-details-social-counts__reactions-count');
      const commentEl = postElement.querySelector('.social-details-social-counts__comments');
      const reactionsCount = reactionEl ? parseInt(reactionEl.innerText.replace(/\D/g, '')) || 0 : 0;
      const commentsCount = commentEl ? parseInt(commentEl.innerText.replace(/\D/g, '')) || 0 : 0;

      return {
        author_name: authorName,
        author_profile_url: authorProfileUrl,
        author_headline: authorHeadline,
        post_text: postText,
        external_link: externalLink,
        post_urn: urn,
        reactions_count: reactionsCount,
        comments_count: commentsCount,
        source: 'tampermonkey_extension',
        timestamp: new Date().toISOString()
      };
    } catch (err) {
      console.error('[n8n Scraper] Error extracting post data:', err);
      return null;
    }
  };

  const sendToN8nWebhook = (payload, buttonEl) => {
    const originalText = buttonEl.innerHTML;
    buttonEl.disabled = true;
    buttonEl.innerHTML = '⏳ Processing...';

    GM_xmlhttpRequest({
      method: 'POST',
      url: webhookUrl,
      headers: {
        'Content-Type': 'application/json'
      },
      data: JSON.stringify(payload),
      timeout: 15000,
      onload: function (response) {
        buttonEl.disabled = false;
        buttonEl.innerHTML = originalText;

        if (response.status >= 200 && response.status < 300) {
          try {
            const resJson = JSON.parse(response.responseText);
            if (resJson.generated_comment) {
              // Copy comment to clipboard and notify
              navigator.clipboard.writeText(resJson.generated_comment);
              showToast(`<b>✅ AI Comment Generated & Copied!</b><br/>"${resJson.generated_comment.substring(0, 80)}..."`);
            } else {
              showToast('<b>✅ Post Sent to n8n Workflow!</b>');
            }
          } catch (e) {
            showToast('<b>✅ Webhook triggered successfully!</b>');
          }
        } else {
          showToast(`<b>❌ Error ${response.status}:</b> Failed to connect to n8n webhook.`, true);
        }
      },
      onerror: function (err) {
        buttonEl.disabled = false;
        buttonEl.innerHTML = originalText;
        showToast('<b>❌ Connection Failed:</b> Make sure n8n is running and webhook URL is active.', true);
      },
      ontimeout: function () {
        buttonEl.disabled = false;
        buttonEl.innerHTML = originalText;
        showToast('<b>⚠️ Timeout:</b> Webhook response took too long.', true);
      }
    });
  };

  const processPostCard = (postContainer) => {
    if (postContainer.dataset.n8nProcessed) return;
    postContainer.dataset.n8nProcessed = 'true';

    // Locate action bar (Like, Comment, Repost, Send bar)
    const actionBar = postContainer.querySelector(
      '.feed-shared-social-action-bar, .social-details-social-counts, .update-v2-social-actions'
    );

    if (!actionBar) return;

    // Create wrapper button
    const btnWrapper = document.createElement('div');
    btnWrapper.className = 'n8n-btn-wrapper';

    const btn = document.createElement('button');
    btn.className = 'n8n-trigger-btn';
    btn.innerHTML = '⚡ Send to n8n AI';
    btn.title = 'Extract post and trigger n8n comment automation';

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      const postData = extractPostData(postContainer);
      if (!postData || !postData.post_text) {
        showToast('<b>⚠️ Warning:</b> Could not extract post text.', true);
        return;
      }

      sendToN8nWebhook(postData, btn);
    });

    btnWrapper.appendChild(btn);
    actionBar.appendChild(btnWrapper);
  };

  const observeLinkedInFeed = () => {
    const scanPosts = () => {
      const posts = document.querySelectorAll(
        'div.feed-shared-update-v2, div[data-urn*="activity"], article'
      );
      posts.forEach(processPostCard);
    };

    // Initial scan
    scanPosts();

    // Observer for lazy-loaded posts
    const observer = new MutationObserver((mutations) => {
      let shouldScan = false;
      for (const mutation of mutations) {
        if (mutation.addedNodes.length > 0) {
          shouldScan = true;
          break;
        }
      }
      if (shouldScan) scanPosts();
    });

    observer.observe(document.body, { childList: true, subtree: true });
  };

  const renderConfigFab = () => {
    const fab = document.createElement('div');
    fab.className = 'n8n-config-fab';
    fab.innerHTML = '⚙️';
    fab.title = 'Configure n8n Webhook URL';

    fab.addEventListener('click', () => {
      const input = prompt('Enter your n8n Webhook URL:', webhookUrl);
      if (input !== null && input.trim() !== '') {
        webhookUrl = input.trim();
        GM_setValue('n8n_webhook_url', webhookUrl);
        showToast(`<b>⚙️ Webhook URL updated:</b><br/>${webhookUrl}`);
      }
    });

    document.body.appendChild(fab);
  };

  const init = () => {
    injectStyles();
    renderConfigFab();
    observeLinkedInFeed();
    console.log('[n8n Scraper] LinkedIn Tampermonkey Assistant initialized successfully.');
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();