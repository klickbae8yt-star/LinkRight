/**
 * LinkedIn Reply Automation - Simplified Chrome Extension
 * Content Script - UI and Smart Engagement
 */

class LinkedInReplyExtension {
    constructor() {
        // Core state
        this.sidebarOpen = false;
        this.extensionActive = false;
        this.smartEngagementEnabled = false;
        this.automationRunning = false;

        // Settings
        this._settings = null;

        // Webhook throttling
        this.webhookInFlight = false;
        this.lastWebhookAt = 0;
        this.webhookCooldownMs = 10000;

        this.init();
    }

    // Lazy getter for settings
    get settings() {
        if (!this._settings) {
            this._settings = this.getDefaultSettings();
        }
        return this._settings;
    }

    set settings(value) {
        this._settings = value;
    }

    /**
     * Default settings
     */
    getDefaultSettings() {
        return {
            // Webhooks (Production URLs)
            webhookCollectComments: 'https://n8n.linkright.in/webhook/collect-comments',
            webhookLeadCategorization: 'https://n8n.linkright.in/webhook/lead-categorization',
            webhookAiReply: 'https://n8n.linkright.in/webhook/linkedin-reply',

            // Scraper Settings
            leadGenKeywords: 'DM',

            // Reply Automation
            googleSheetsId: '19ziyAH5xJeAF8fW4Kb31gzrv0_Lluiuw9NGGan6xIKc',

            // Message templates
            messageConnected: "Thanks for your interest! Sending you the resource via DM now. Check your messages! 📩",
            messageNotConnected: "Hey! We're not connected yet. Please send me a connection request and DM me with 'GEMINI' - I'll send you the resource right away! 🚀",
            messagePending: "Hey! I see you've sent a connection request. I'll accept it shortly and send you the resource via DM! 👍",

            // Backend
            backendUrl: 'http://127.0.0.1:3000'
        };
    }

    /**
     * Initialize extension
     */
    async init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    /**
     * Setup extension
     */
    async setup() {
        console.log('LinkedIn Reply Extension: Setting up...');

        // Wait for LinkedIn to load
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Load settings
        await this.loadSettings();

        // Create sidebar
        this.createSidebar();

        // Setup event listeners
        this.setupEventListeners();

        console.log('LinkedIn Reply Extension: Ready');
    }

    /**
     * Load settings from storage
     */
    async loadSettings() {
        try {
            const response = await chrome.runtime.sendMessage({
                type: 'LOAD_SETTINGS'
            });

            if (response && response.success && response.settings) {
                this.settings = { ...this.getDefaultSettings(), ...response.settings };
            } else {
                this.settings = this.getDefaultSettings();
            }
        } catch (error) {
            console.warn('Failed to load settings:', error);
            this.settings = this.getDefaultSettings();
        }
    }

    /**
     * Save settings to storage
     */
    async saveSettings() {
        try {
            await chrome.runtime.sendMessage({
                type: 'SAVE_SETTINGS',
                settings: this.settings
            });
        } catch (error) {
            console.error('Failed to save settings:', error);
        }
    }

    /**
     * Create sidebar UI
     */
    createSidebar() {
        // Remove existing sidebar
        const existing = document.getElementById('linkedin-reply-sidebar');
        if (existing) existing.remove();

        const sidebar = document.createElement('div');
        sidebar.id = 'linkedin-reply-sidebar';
        sidebar.className = 'linkedin-reply-sidebar';

        sidebar.innerHTML = `
      <div class="lr-sidebar-header">
        <div class="lr-title">LinkedIn Reply</div>
        <button class="lr-close-btn" title="Close">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
      </div>
      
      <div class="lr-sidebar-content">
        <!-- Smart Engagement Section -->
        <div class="lr-section">
          <div class="lr-section-header">
            <h3>💬 Smart Engagement</h3>
            <label class="lr-toggle">
              <input type="checkbox" id="lr-smart-engagement-toggle" ${this.smartEngagementEnabled ? 'checked' : ''}>
              <span class="lr-toggle-slider"></span>
            </label>
          </div>
          <p class="lr-description">AI-powered manual comments via webhook</p>
        </div>
        
        <!-- Reply Automation Section -->
        <div class="lr-section">
          <div class="lr-section-header">
            <h3>🤖 Workflow Controls</h3>
          </div>
          <p class="lr-description">Execute steps in order:</p>
          
          <!-- Step 0: Expand Comments -->
          <button id="lr-expand-comments" class="lr-btn lr-btn-secondary" style="margin-bottom: 10px; border-color: #0ea5e9; color: #0ea5e9;">
            0. Expand Comments (Safe)
          </button>

          <!-- Step 1: Scrape -->
          <button id="lr-scrape-console" class="lr-btn lr-btn-primary" style="margin-bottom: 10px;">
            1. Scrape Console (Copy Data)
          </button>

          <!-- Step 2: Categorize -->
          <button id="lr-start-categorization" class="lr-btn lr-btn-secondary" style="margin-bottom: 10px;">
            2. Start Lead Categorization
          </button>

          <!-- Step 3: Reply Automation -->
          <button id="lr-start-automation" class="lr-btn lr-btn-secondary" style="margin-bottom: 10px;">
            3. Start Reply Automation
          </button>
          
          <!-- Step 4: DM Workflow -->
          <button id="lr-start-dm-flow" class="lr-btn lr-btn-secondary">
            4. Start DM Workflow
          </button>
          
          <div id="lr-automation-status" class="lr-status" style="display: none; margin-top: 16px;">
            <div class="lr-status-text">Idle</div>
            <div class="lr-progress-bar">
              <div class="lr-progress-fill" style="width: 0%"></div>
            </div>
            <div class="lr-progress-text">0/0 comments processed</div>
          </div>
        </div>
        
        <!-- Settings Section -->
        <div class="lr-section lr-settings-section">
          <div class="lr-section-header lr-collapsible" id="lr-settings-toggle">
            <h3>⚙️ Settings</h3>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" class="lr-chevron">
              <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
            </svg>
          </div>
          
          <div class="lr-settings-content" style="display: none;">
            <div class="lr-form-group">
              <label>Smart Engagement Webhook</label>
              <input type="text" id="lr-webhook-url" value="${this.settings.smartEngagementWebhook}" placeholder="https://...">
            </div>
            
            <div class="lr-form-group">
              <label>Google Sheets ID</label>
              <input type="text" id="lr-sheets-id" value="${this.settings.googleSheetsId}" placeholder="1ABC...XYZ">
            </div>
            
            <div class="lr-form-group">
              <label>Backend URL</label>
              <input type="text" id="lr-backend-url" value="${this.settings.backendUrl}" placeholder="http://127.0.0.1:3001">
            </div>

            <div class="lr-section-header" style="margin-top: 16px; margin-bottom: 8px;">
              <h3 style="font-size: 14px;">🔗 Webhook Configuration</h3>
            </div>

            <div class="lr-form-group">
              <label>1. Collect Comments Webhook (Scraper)</label>
              <input type="text" id="lr-webhook-collect" value="${this.settings.webhookCollectComments}" placeholder="https://...">
            </div>

            <div class="lr-form-group">
              <label>2. Lead Categorization Webhook</label>
              <input type="text" id="lr-webhook-categorization" value="${this.settings.webhookLeadCategorization}" placeholder="https://...">
            </div>

            <div class="lr-form-group">
              <label>3. AI Reply Webhook (Smart Engagement)</label>
              <input type="text" id="lr-webhook-ai-reply" value="${this.settings.webhookAiReply}" placeholder="https://...">
            </div>

            <div class="lr-section-header" style="margin-top: 16px; margin-bottom: 8px;">
              <h3 style="font-size: 14px;">🛠️ Scraper Settings</h3>
            </div>

            <div class="lr-form-group">
              <label>Lead Gen Keywords (comma separated)</label>
              <textarea id="lr-lead-keywords" rows="2" placeholder="co-founder, hiring">${this.settings.leadGenKeywords}</textarea>
            </div>
            
            <div class="lr-form-group">
              <label>Message (Connected)</label>
              <textarea id="lr-msg-connected" rows="2">${this.settings.messageConnected}</textarea>
            </div>
            
            <div class="lr-form-group">
              <label>Message (Not Connected)</label>
              <textarea id="lr-msg-not-connected" rows="2">${this.settings.messageNotConnected}</textarea>
            </div>
            
            <div class="lr-form-group">
              <label>Message (Pending)</label>
              <textarea id="lr-msg-pending" rows="2">${this.settings.messagePending}</textarea>
            </div>
            
            <button id="lr-save-settings" class="lr-btn lr-btn-secondary">Save Settings</button>
          </div>
        </div>
      </div>
    `;

        document.body.appendChild(sidebar);
        this.sidebar = sidebar;

        // Add event listeners
        this.addSidebarEventListeners();
    }

    /**
     * Add sidebar event listeners
     */
    addSidebarEventListeners() {
        // Close button
        const closeBtn = this.sidebar.querySelector('.lr-close-btn');
        closeBtn.addEventListener('click', () => this.closeSidebar());

        // Smart Engagement toggle
        const smartToggle = this.sidebar.querySelector('#lr-smart-engagement-toggle');
        smartToggle.addEventListener('change', (e) => {
            this.smartEngagementEnabled = e.target.checked;
            if (this.smartEngagementEnabled) {
                this.enableSmartEngagement();
            } else {
                this.disableSmartEngagement();
            }
        });

        // Expand Comments button
        const expandBtn = this.sidebar.querySelector('#lr-expand-comments');
        expandBtn.addEventListener('click', () => this.expandCommentsSafe());

        // Scrape Console button
        const scrapeBtn = this.sidebar.querySelector('#lr-scrape-console');
        scrapeBtn.addEventListener('click', () => this.scrapeConsole());

        // Start categorization button
        const catBtn = this.sidebar.querySelector('#lr-start-categorization');
        catBtn.addEventListener('click', () => this.startLeadCategorization());

        // Start automation button
        const startBtn = this.sidebar.querySelector('#lr-start-automation');
        startBtn.addEventListener('click', () => this.startReplyAutomation());

        // Start DM Workflow button
        const dmBtn = this.sidebar.querySelector('#lr-start-dm-flow');
        dmBtn.addEventListener('click', () => {
            alert('DM Workflow trigger not configured yet.');
        });

        // Settings toggle
        const settingsToggle = this.sidebar.querySelector('#lr-settings-toggle');
        const settingsContent = this.sidebar.querySelector('.lr-settings-content');
        settingsToggle.addEventListener('click', () => {
            const isOpen = settingsContent.style.display !== 'none';
            settingsContent.style.display = isOpen ? 'none' : 'block';
            settingsToggle.classList.toggle('open', !isOpen);
        });

        // Save settings button
        const saveBtn = this.sidebar.querySelector('#lr-save-settings');
        saveBtn.addEventListener('click', () => this.saveSettingsFromUI());
    }

    /**
     * Safe Comment Expander
     */
    async expandCommentsSafe() {
        const btn = this.sidebar.querySelector('#lr-expand-comments');

        // Toggle Stop
        if (btn.textContent.includes('Stop')) {
            this.stopExpansion = true;
            btn.textContent = 'Stopping...';
            return;
        }

        this.stopExpansion = false;
        const originalText = btn.textContent;
        btn.textContent = '🛑 Stop Expanding';
        btn.classList.remove('lr-btn-secondary');
        btn.classList.add('lr-btn-primary'); // Make it red/prominent (using primary for now)

        try {
            console.log('🚀 Starting Safe Expansion...');
            let totalExpanded = 0;
            // No batch limit - expand all

            while (!this.stopExpansion) {
                // Find buttons (refresh list every time as DOM changes)
                // FIXED: More specific selectors to avoid matching search bar etc.
                const selectors = [
                    // Load more comments buttons (primary)
                    '.comments-comments-list__load-more-comments-button',
                    '.comments-comments-list__load-more-comments-button--cr',
                    // See previous/more replies buttons
                    '.comments-replies-list__replies-button',
                    // Show replies button (alternative class)
                    '.show-prev-replies',
                    // Generic show more in comments section
                    '[data-test-comments-comment-item__show-replies-button]'
                ];

                // Get all buttons matching selectors
                let buttons = Array.from(document.querySelectorAll(selectors.join(', ')));

                // ALSO: Find buttons with text containing "replies" or "previous" but ONLY inside comments section
                const commentsSection = document.querySelector('.comments-comments-list, .comments-comment-list, [class*="comments"]');
                if (commentsSection) {
                    const textButtons = Array.from(commentsSection.querySelectorAll('button')).filter(btn => {
                        const text = btn.textContent.toLowerCase();
                        return (text.includes('replies') || text.includes('previous') || text.includes('more')) &&
                            !text.includes('react') && !text.includes('like') && !text.includes('collapse'); // Exclude collapse & reaction buttons
                    });
                    buttons = [...buttons, ...textButtons];
                }

                // Remove duplicates
                buttons = [...new Set(buttons)];

                // Filter: visible buttons AND inside comments section AND not collapse buttons
                const visibleButtons = buttons.filter(b => {
                    if (b.offsetParent === null) return false;
                    // Ensure button is inside a comments-related container
                    const isInComments = b.closest('.comments-comments-list, .comments-comment-item, [class*="comment"]');
                    if (!isInComments) return false;
                    // CRITICAL: Exclude "Collapse" buttons
                    const buttonText = b.textContent.toLowerCase();
                    if (buttonText.includes('collapse')) return false;
                    return true;
                });

                if (visibleButtons.length === 0) {
                    console.log('✅ No more buttons found.');
                    break;
                }

                const buttonToClick = visibleButtons[0]; // Take first one
                console.log(`🔍 Found button: "${buttonToClick.textContent.trim().substring(0, 50)}"`);

                // Scroll into view
                buttonToClick.scrollIntoView({ behavior: 'smooth', block: 'center' });

                // Click
                buttonToClick.click();
                totalExpanded++;
                console.log(`Clicked button ${totalExpanded}`);

                // Random Delay (2-5 seconds)
                const delay = Math.floor(Math.random() * 3000) + 2000;
                await new Promise(r => setTimeout(r, delay));
            }

            if (this.stopExpansion) {
                console.log('🛑 Expansion stopped by user.');
                btn.textContent = 'Stopped';
            } else {
                console.log('✅ Expansion Complete');
                btn.textContent = '✓ All Expanded';
            }

        } catch (error) {
            console.error('Expansion failed:', error);
            btn.textContent = '❌ Error';
        } finally {
            setTimeout(() => {
                btn.textContent = originalText;
                btn.classList.remove('lr-btn-primary');
                btn.classList.add('lr-btn-secondary');
                this.stopExpansion = false;
            }, 3000);
        }
    }

    /**
     * Scrape Console and Copy to Clipboard + Webhook
     */
    async scrapeConsole() {
        const btn = this.sidebar.querySelector('#lr-scrape-console');
        const originalText = btn.textContent;
        btn.textContent = 'Scraping...';
        btn.disabled = true;

        try {
            console.log('🚀 Starting LinkedIn comment extraction...');
            const comments = [];
            const seen = new Set();

            // Parse Keywords
            const keywords = this.settings.leadGenKeywords
                .split(',')
                .map(k => k.trim().toLowerCase())
                .filter(k => k.length > 0);

            console.log('🔍 Checking for keywords:', keywords);

            // Get current post URL and title
            const postUrl = window.location.href;
            const postTitle = document.querySelector('.feed-shared-update-v2__description')?.textContent.trim().substring(0, 100) || 'LinkedIn Post';

            // Find all comment articles
            const commentElements = document.querySelectorAll('article.comments-comment-entity');
            console.log(`📊 Found ${commentElements.length} comment elements`);

            commentElements.forEach(article => {
                try {
                    // Get unique comment ID
                    const commentId = article.getAttribute('data-id');

                    // Skip duplicates
                    if (!commentId || seen.has(commentId)) return;
                    seen.add(commentId);

                    // Determine Type (Parent vs Reply)
                    const isReply = article.classList.contains('comments-comment-entity--reply');
                    const commentType = isReply ? 'Reply' : 'Parent';

                    // Extract all fields
                    const nameEl = article.querySelector('.comments-comment-meta__description-title');
                    const commenterName = nameEl ? nameEl.textContent.trim() : '';

                    const profileEl = article.querySelector('a.comments-comment-meta__description-container');
                    let commenterProfileUrl = profileEl ? profileEl.getAttribute('href') : '';
                    if (commenterProfileUrl && !commenterProfileUrl.startsWith('http')) {
                        commenterProfileUrl = 'https://www.linkedin.com' + commenterProfileUrl;
                    }

                    const headlineEl = article.querySelector('.comments-comment-meta__description-subtitle');
                    const commenterHeadline = headlineEl ? headlineEl.textContent.trim() : '';

                    const textEl = article.querySelector('.comments-comment-item__main-content');
                    const commentText = textEl ? textEl.textContent.trim() : '';

                    const timeEl = article.querySelector('time.comments-comment-meta__data');
                    const timestamp = timeEl ? timeEl.textContent.trim() : '';

                    // Build proper LinkedIn comment URL
                    let commentUrl = '';
                    if (commentId) {
                        const typeMatch = commentId.match(/(activity|ugcPost):(\d+)/);
                        const commentMatch = commentId.match(/,(\d+)\)/);

                        if (typeMatch && commentMatch) {
                            const postType = typeMatch[1];
                            const postId = typeMatch[2];
                            const commentOnlyId = commentMatch[1];
                            const encodedCommentUrn = `urn%3Ali%3Acomment%3A%28${postType}%3A${postId}%2C${commentOnlyId}%29`;
                            const encodedDashCommentUrn = `urn%3Ali%3Afsd_comment%3A%28${commentOnlyId}%2Curn%3Ali%3A${postType}%3A${postId}%29`;
                            commentUrl = `https://www.linkedin.com/feed/update/urn:li:${postType}:${postId}?commentUrn=${encodedCommentUrn}&dashCommentUrn=${encodedDashCommentUrn}`;
                        }
                    }

                    // Current timestamp
                    const now = new Date();
                    const timestampCaptured = now.toISOString().replace('T', ' ').substring(0, 19);

                    // Connection Degree
                    const metaData = article.querySelector('.comments-comment-meta__data');
                    const metaText = metaData ? metaData.textContent : article.textContent;
                    let connectionDegree = 'None';
                    if (metaText.includes('• 1st')) connectionDegree = '1st';
                    else if (metaText.includes('• 2nd')) connectionDegree = '2nd';
                    else if (metaText.includes('• 3rd')) connectionDegree = '3rd';

                    // Keyword Matching
                    let matchedKeyword = '';
                    const lowerText = commentText.toLowerCase();
                    for (const kw of keywords) {
                        if (lowerText.includes(kw)) {
                            matchedKeyword = kw;
                            break;
                        }
                    }

                    if (commenterName && commentText) {
                        // Construct object with ALL columns (A-Z) in correct order
                        comments.push({
                            // Basic Info
                            Row_ID: '', // A: Formula in Sheet
                            Timestamp_Captured: timestampCaptured, // B
                            Post_URL: postUrl, // C
                            Post_Title: postTitle, // D
                            Commenter_Name: commenterName, // E
                            Commenter_Profile_URL: commenterProfileUrl, // F
                            Commenter_Headline: commenterHeadline, // G
                            Comment_Text: commentText, // H
                            Comment_URL: commentUrl, // I
                            Lead_Magnet_Keyword: matchedKeyword, // J
                            AI_Category: '', // K
                            Processing_Status: 'New', // L

                            // Status & Automation (Defaults)
                            Connection_Status: connectionDegree, // M
                            Comment_Reply_Sent: 'No', // N
                            Comment_Reply_Text: '', // O
                            Comment_Reply_Timestamp: '', // P
                            DM_Sent: 'No', // Q
                            DM_Sent_Timestamp: '', // R
                            Lead_Magnet_Delivered: 'No', // S
                            Error_Log: '', // T
                            Last_Updated: '', // U
                            Notes: '', // V

                            // State Management
                            Comment_ID: commentId, // W
                            Comment_Type: commentType, // X
                            Active_Workflow: '', // Y
                            Workflow_Status: '' // Z
                        });
                    }
                } catch (err) {
                    console.error('Error processing comment:', err);
                }
            });

            // 1. Convert to CSV for Clipboard
            const headers = Object.keys(comments[0] || {}).join(',');
            const rows = comments.map(c => Object.values(c).map(v => `"${String(v).replace(/"/g, '""')}"`).join(','));
            const csvString = [headers, ...rows].join('\n');

            await navigator.clipboard.writeText(csvString);
            console.log(`✅ Copied ${comments.length} items to Clipboard (CSV)!`);

            // 2. Send JSON to Webhook (via background.js to bypass CORS)
            const webhookUrl = this.settings.webhookCollectComments;
            console.log(`📤 Sending data to Webhook: ${webhookUrl}`);

            try {
                const response = await chrome.runtime.sendMessage({
                    type: 'FETCH_WEBHOOK',
                    url: webhookUrl,
                    method: 'POST',
                    body: { comments }
                });

                if (response.success) {
                    console.log('✅ Webhook success!');
                    btn.textContent = `✓ Copied CSV & Sent to Webhook!`;
                } else {
                    console.error('Webhook failed:', response.error);
                    btn.textContent = `✓ Copied CSV (Webhook Failed)`;
                }
            } catch (webhookErr) {
                console.error('Webhook error:', webhookErr);
                btn.textContent = `✓ Copied CSV (Webhook Error)`;
            }

        } catch (error) {
            console.error('Scraping failed:', error);
            btn.textContent = '❌ Failed';
            alert('Scraping failed. Check console.');
        } finally {
            setTimeout(() => {
                btn.disabled = false;
                btn.textContent = originalText;
            }, 3000);
        }
    }

    /**
 * Start Lead Categorization
 */
    async startLeadCategorization() {
        const btn = this.sidebar.querySelector('#lr-start-categorization');
        const originalText = btn.textContent;

        btn.disabled = true;
        btn.textContent = 'Triggering...';

        try {
            // Direct Webhook Call with Keywords
            const response = await fetch(this.settings.webhookLeadCategorization, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    trigger: 'manual_extension',
                    keywords: this.settings.leadGenKeywords // Send keywords to n8n
                })
            });

            if (response.ok) {
                btn.textContent = '✓ Triggered!';
            } else {
                throw new Error(`Webhook failed: ${response.status}`);
            }
        } catch (error) {
            console.error('Failed to trigger categorization:', error);
            btn.textContent = '❌ Failed';
            alert('Failed to trigger lead categorization. Check console for details.');
        } finally {
            setTimeout(() => {
                btn.disabled = false;
                btn.textContent = originalText;
            }, 3000);
        }
    }

    /**
     * Setup global event listeners
     */
    setupEventListeners() {
        // Listen for messages from background script
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            if (message.type === 'OPEN_SIDEBAR') {
                this.openSidebar();
                sendResponse({ success: true });
            } else if (message.type === 'AUTOMATION_PROGRESS') {
                this.updateAutomationProgress(message.data);
                sendResponse({ success: true });
            } else if (message.type === 'AUTOMATION_COMPLETE') {
                this.automationComplete(message.data);
                sendResponse({ success: true });
            }
            return true;
        });
    }

    /**
     * Open sidebar
     */
    openSidebar() {
        if (!this.sidebar) this.createSidebar();
        this.sidebar.classList.add('open');
        this.sidebarOpen = true;
        this.extensionActive = true;

        // Update icon
        chrome.runtime.sendMessage({ type: 'UPDATE_ICON', active: true });
    }

    /**
     * Close sidebar
     */
    closeSidebar() {
        this.sidebar.classList.remove('open');
        this.sidebarOpen = false;
        this.extensionActive = false;

        // Update icon
        chrome.runtime.sendMessage({ type: 'UPDATE_ICON', active: false });
    }

    /**
     * Enable Smart Engagement
     */
    enableSmartEngagement() {
        console.log('Smart Engagement enabled');
        // Listen for comment box focus (Auto-trigger)
        document.addEventListener('focusin', this.handleFocusIn.bind(this));

        // Listen for Shortcut (Cmd+Shift+.)
        this.boundHandleKeydown = this.handleKeydown.bind(this);
        document.addEventListener('keydown', this.boundHandleKeydown);
    }

    /**
     * Disable Smart Engagement
     */
    disableSmartEngagement() {
        console.log('Smart Engagement disabled');
        document.removeEventListener('focusin', this.handleFocusIn.bind(this));

        if (this.boundHandleKeydown) {
            document.removeEventListener('keydown', this.boundHandleKeydown);
        }
    }

    /**
     * Handle Keydown (Shortcut: Cmd+Shift+.)
     */
    async handleKeydown(event) {
        // Check for Cmd+Shift+. (Mac) or Ctrl+Shift+. (Windows)
        if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key === '.') {
            console.log('⌨️ Shortcut detected: Cmd+Shift+.');
            event.preventDefault(); // Prevent default browser behavior

            // Find focused editor
            const editor = document.activeElement.closest('.ql-editor, [contenteditable="true"]');
            if (!editor) {
                console.log('❌ No active editor found for shortcut.');
                return;
            }

            // Extract post data
            const postData = this.extractPostData(editor);
            if (!postData) {
                console.log('❌ Could not extract post data.');
                return;
            }

            // Call webhook
            console.log('🚀 Triggering AI Reply via Shortcut...');
            await this.callSmartEngagementWebhook(editor, postData);
        }
    }

    /**
     * Handle focus in event (for Smart Engagement)
     */
    async handleFocusIn(event) {
        if (!this.smartEngagementEnabled) return;

        // Check if focused element is a LinkedIn comment editor
        const editor = event.target.closest('.ql-editor, [contenteditable="true"]');
        if (!editor) return;

        // Check if it's a comment/reply box
        const isCommentBox = editor.closest('[data-test-id*="comment"], [aria-label*="comment" i], [aria-label*="reply" i]');
        if (!isCommentBox) return;

        // Throttle webhook calls
        if (this.webhookInFlight) {
            console.log('Webhook in flight, skipping');
            return;
        }

        if (Date.now() - this.lastWebhookAt < this.webhookCooldownMs) {
            console.log('Webhook cooldown active, skipping');
            return;
        }

        // Extract post data
        const postData = this.extractPostData(editor);
        if (!postData) {
            console.log('Could not extract post data');
            return;
        }

        // Call webhook
        await this.callSmartEngagementWebhook(editor, postData);
    }

    /**
     * Extract post data from editor context
     */
    /**
     * Extract post data from editor context (Rich Data)
     */
    extractPostData(editor) {
        try {
            // Find parent post container (supports both activity and ugcPost)
            const postContainer = editor.closest('[data-id^="urn:li:activity:"], [data-id^="urn:li:ugcPost:"], .feed-shared-update-v2');

            if (!postContainer) {
                console.log('⚠️ No post container found. Trying fallback...');
                return null;
            }

            // 1. Root Post ID
            const rootPostId = postContainer.getAttribute('data-id') || postContainer.getAttribute('data-urn') || '';

            // 2. Root Post Text
            const textElement = postContainer.querySelector('.feed-shared-update-v2__description .update-components-text') ||
                postContainer.querySelector('.feed-shared-text') ||
                postContainer.querySelector('.feed-shared-update-v2__description');
            const postText = textElement ? textElement.innerText.trim() : '';

            // 3. Root Post Author
            const authorElement = postContainer.querySelector('.update-components-actor__name') ||
                postContainer.querySelector('.feed-shared-actor__name');
            const authorName = authorElement ? authorElement.innerText.trim() : 'Unknown';

            // 4. Engagement Stats
            const likesElement = postContainer.querySelector('.social-details-social-counts__reactions-count');
            const commentsElement = postContainer.querySelector('.social-details-social-counts__comments');

            const likes = likesElement ? parseInt(likesElement.innerText.replace(/[^0-9]/g, '')) || 0 : 0;
            const comments = commentsElement ? parseInt(commentsElement.innerText.replace(/[^0-9]/g, '')) || 0 : 0;

            // 5. Thread ID (If replying to a comment)
            let threadId = '';
            const parentComment = editor.closest('article.comments-comment-entity');
            if (parentComment) {
                threadId = parentComment.getAttribute('data-id') || '';
            }

            // 6. Time Since Posted
            const timeElement = postContainer.querySelector('.update-components-actor__sub-description') ||
                postContainer.querySelector('.feed-shared-actor__sub-description');
            const timeSincePosted = timeElement ? timeElement.innerText.trim().split('•')[0].trim() : '';

            // Construct Rich Payload matching EXACTLY the old extension structure
            return {
                // Metadata
                thread_id: threadId,
                root_post_id: rootPostId,
                triggered_by: 'manual_shortcut', // Distinct from 'hotkey'
                timestamp: new Date().toISOString(),
                locale: navigator.language || 'en-US',
                action_type: 'reply', // Default action
                user_override_flags: {}, // Placeholder for future flags

                // Root post author
                root_post_author: { name: authorName },

                // Post information
                post_text: postText,
                post_media_type: 'unknown', // Placeholder
                post_engagement_numbers: { likes, comments, reposts: 0 },
                time_since_posted: timeSincePosted,

                // Comments (Empty for manual shortcut context, as we are writing a NEW comment)
                all_comments: [],

                // Personalization & Context
                comment_depth_level: threadId ? 1 : 0, // 0 = Top level, 1 = Reply
                parent_author_headline: '', // Could scrape if needed
                comment_engagement_count: 0,
                thread_visibility_state: 'visible',

                // Legacy fields for backward compatibility
                postId: rootPostId,
                postContent: postText,
                author: authorName
            };
        } catch (error) {
            console.error('Error extracting post data:', error);
            return null;
        }
    }

    /**
     * Call Smart Engagement webhook (via background.js to bypass CORS)
     */
    async callSmartEngagementWebhook(editor, postData) {
        this.webhookInFlight = true;
        this.lastWebhookAt = Date.now();

        console.log('📤 Calling AI Reply webhook with:', postData);

        try {
            const response = await chrome.runtime.sendMessage({
                type: 'FETCH_WEBHOOK',
                url: this.settings.webhookAiReply,
                method: 'POST',
                body: postData
            });

            if (!response.success) {
                throw new Error(response.error || 'Webhook failed');
            }

            const data = response.data;
            console.log('📥 Webhook response:', data);

            if (data.comment) {
                // Insert AI-generated comment
                editor.textContent = data.comment;
                editor.dispatchEvent(new Event('input', { bubbles: true }));
                console.log('✅ AI comment inserted successfully!');
            } else {
                console.warn('⚠️ Webhook returned no "comment" field. Response:', data);
                alert('AI Reply webhook did not return a comment. Check n8n workflow.');
            }
        } catch (error) {
            console.error('❌ Smart Engagement webhook error:', error);
            alert('Failed to get AI reply. Check console for details.');
        } finally {
            this.webhookInFlight = false;
        }
    }

    /**
     * Start Reply Automation
     */
    async startReplyAutomation() {
        if (this.automationRunning) {
            console.log('Automation already running');
            return;
        }

        // Validate settings
        if (!this.settings.googleSheetsId) {
            alert('Please configure Google Sheets ID in Settings');
            return;
        }

        this.automationRunning = true;

        // Show status
        const statusDiv = this.sidebar.querySelector('#lr-automation-status');
        statusDiv.style.display = 'block';
        statusDiv.querySelector('.lr-status-text').textContent = 'Starting...';

        // Disable button
        const startBtn = this.sidebar.querySelector('#lr-start-automation');
        startBtn.disabled = true;
        startBtn.textContent = 'Running...';

        try {
            // Call backend to start automation
            const response = await fetch(`${this.settings.backendUrl}/api/reply-automation/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sheetsId: this.settings.googleSheetsId,
                    messages: {
                        connected: this.settings.messageConnected,
                        notConnected: this.settings.messageNotConnected,
                        pending: this.settings.messagePending
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`Backend error: ${response.status}`);
            }

            const result = await response.json();
            console.log('Automation started:', result);

        } catch (error) {
            console.error('Failed to start automation:', error);
            alert(`Failed to start automation: ${error.message}`);

            // Reset UI
            statusDiv.style.display = 'none';
            startBtn.disabled = false;
            startBtn.textContent = 'Start Reply Automation';
            this.automationRunning = false;
        }
    }

    /**
     * Update automation progress
     */
    updateAutomationProgress(data) {
        const statusDiv = this.sidebar.querySelector('#lr-automation-status');
        const { current, total, status } = data;

        statusDiv.querySelector('.lr-status-text').textContent = status;
        statusDiv.querySelector('.lr-progress-fill').style.width = `${(current / total) * 100}%`;
        statusDiv.querySelector('.lr-progress-text').textContent = `${current}/${total} comments processed`;
    }

    /**
     * Automation complete
     */
    automationComplete(data) {
        const statusDiv = this.sidebar.querySelector('#lr-automation-status');
        const startBtn = this.sidebar.querySelector('#lr-start-automation');

        statusDiv.querySelector('.lr-status-text').textContent = 'Complete!';
        statusDiv.querySelector('.lr-progress-fill').style.width = '100%';
        statusDiv.querySelector('.lr-progress-text').textContent = `${data.total} comments processed (${data.successful} successful)`;

        // Re-enable button
        setTimeout(() => {
            startBtn.disabled = false;
            startBtn.textContent = 'Start Reply Automation';
            this.automationRunning = false;

            // Hide status after 5 seconds
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }, 2000);
    }

    /**
     * Save settings from UI
     */
    async saveSettingsFromUI() {
        // this.settings.smartEngagementWebhook is now webhookAiReply
        this.settings.googleSheetsId = this.sidebar.querySelector('#lr-sheets-id').value;
        this.settings.backendUrl = this.sidebar.querySelector('#lr-backend-url').value;

        this.settings.webhookCollectComments = this.sidebar.querySelector('#lr-webhook-collect').value;
        this.settings.webhookLeadCategorization = this.sidebar.querySelector('#lr-webhook-categorization').value;
        this.settings.webhookAiReply = this.sidebar.querySelector('#lr-webhook-ai-reply').value;

        this.settings.leadGenKeywords = this.sidebar.querySelector('#lr-lead-keywords').value;

        this.settings.messageConnected = this.sidebar.querySelector('#lr-msg-connected').value;
        this.settings.messageNotConnected = this.sidebar.querySelector('#lr-msg-not-connected').value;
        this.settings.messagePending = this.sidebar.querySelector('#lr-msg-pending').value;

        await this.saveSettings();

        // Show confirmation
        const saveBtn = this.sidebar.querySelector('#lr-save-settings');
        const originalText = saveBtn.textContent;
        saveBtn.textContent = '✓ Saved!';
        setTimeout(() => {
            saveBtn.textContent = originalText;
        }, 2000);
    }
}

// Initialize extension
const linkedInReplyExtension = new LinkedInReplyExtension();
