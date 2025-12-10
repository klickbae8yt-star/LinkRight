/**
 * LinkedIn Comment Reply Automation
 * 
 * Features:
 * - Rich Data Extraction (Root Post, Author, Stats)
 * - Logic based on Connection Degree & Keywords
 * - Simplified "Paste & Post" Navigation
 * - AI Reply generation via Webhook (Rich Payload)
 * - Local Server Trigger
 */

const { chromium } = require('playwright');
const fs = require('fs');
const axios = require('axios');

// Configuration
const CONFIG = {
    SESSION_FILE: './execution/linkedin_session.json',
    HEADLESS: false,
    SLOW_MO: 100,
    WEBHOOK_URL: 'https://n8n.linkright.in/webhook-test/smart-reply', // Updated to Test URL
    MESSAGES: {
        CONNECT_REQUEST: "Hey! We're not connected yet. Please send me a connection request so I can send you the resource! 🚀"
    }
};

// Utility: Random delay
function randomDelay(min = 2000, max = 4000) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Utility: Sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Utility: Logging
function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level}] ${message}`);
}

// --- DATA EXTRACTION FUNCTIONS ---

/**
 * Extract Root Post Data (Text, Author, Stats)
 * Scrolls up to find the main post container.
 */
async function extractRootPostData(page) {
    log('Extracting Root Post Data...');
    try {
        // Scroll up a bit to ensure main post is in DOM
        await page.evaluate(() => window.scrollTo(0, 0));
        await sleep(1000);

        const rootData = await page.evaluate(() => {
            // Try to find the main post container
            // Strategy: Look for the 'feed-shared-update-v2' or similar container
            const postContainer = document.querySelector('.feed-shared-update-v2') ||
                document.querySelector('div[data-urn^="urn:li:activity:"]');

            if (!postContainer) return null;

            // 1. Root Post ID
            const rootPostId = postContainer.getAttribute('data-urn') || '';

            // 2. Root Post Text
            const textElement = postContainer.querySelector('.feed-shared-update-v2__description .update-components-text') ||
                postContainer.querySelector('.feed-shared-text');
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

            return {
                root_post_id: rootPostId,
                post_text: postText,
                root_post_author: { name: authorName },
                post_engagement_numbers: { likes, comments, reposts: 0 }
            };
        });

        if (rootData) {
            log(`✅ Root Post Data Extracted: ${rootData.root_post_author.name}`);
            return rootData;
        } else {
            log('⚠️ Could not find Root Post Data (Might be a direct comment URL)', 'WARN');
            return null;
        }

    } catch (error) {
        log(`Error extracting root post data: ${error.message}`, 'ERROR');
        return null;
    }
}

/**
 * Extract Thread Context (Previous Comments)
 * Useful if replying to a nested comment.
 */
async function extractThreadContext(page, commentUrnId) {
    // Placeholder: For now, we assume we are replying to a top-level comment
    // Future: Implement logic to scrape parent comments if connectionDegree is '2nd' or '3rd'
    return [];
}

// --- ACTION FUNCTIONS ---

// Post reply using Simplified "Paste & Post" Logic
async function postReply(page, commentUrl, message, commentUrnId) {
    log(`Posting reply to: ${commentUrl} | ID: ${commentUrnId}`);

    try {
        // 1. Go to URL
        await page.goto(commentUrl, { waitUntil: 'domcontentloaded' });
        log('Page loaded, waiting for scroll...');
        await sleep(randomDelay(5000, 8000));

        // 2. Click 'Reply' button (Simple Selector)
        // We assume the URL opens the specific comment and the 'Reply' button is visible
        log('Looking for Reply button...');

        // Try specific comment's reply button first
        const replySelector = `article[data-id="${commentUrnId}"] button.artdeco-button--tertiary`;
        // Fallback to any visible reply button if specific one fails (risky but often works for single comment view)
        const fallbackSelector = 'button.reply';

        let replyButton = await page.$(replySelector);

        if (!replyButton) {
            // Try finding by text "Reply" inside the specific article
            replyButton = await page.evaluateHandle((urn) => {
                const article = document.querySelector(`article[data-id="${urn}"]`);
                if (!article) return null;
                const buttons = Array.from(article.querySelectorAll('button'));
                return buttons.find(b => b.innerText.trim().toLowerCase() === 'reply');
            }, commentUrnId);
        }

        if (replyButton) {
            await replyButton.click();
            log('Clicked Reply button');
        } else {
            log('⚠️ Specific Reply button not found, trying generic focus...', 'WARN');
            // Fallback: Just press 'R' (LinkedIn shortcut) if enabled, or Tab navigation
        }

        await sleep(randomDelay(1500, 2500));

        // 3. Paste Message
        log(`Pasting message...`);

        // Type the message (more human-like than paste)
        await page.keyboard.type(message, { delay: 50 });
        await sleep(randomDelay(1000, 2000));

        // 4. Tab -> Tab -> Tab -> Enter (To Post)
        log('Pressing Tab (3x) to reach Post button...');
        await page.keyboard.press('Tab');
        await sleep(300);
        await page.keyboard.press('Tab');
        await sleep(300);
        await page.keyboard.press('Tab');
        await sleep(300);

        // 5. Enter to Post
        log('Pressing Enter to Post...');
        await page.keyboard.press('Enter');

        await sleep(randomDelay(3000, 5000));
        log('Reply posted successfully!', 'SUCCESS');
        return true;

    } catch (error) {
        log(`Error posting reply: ${error.message}`, 'ERROR');
        return false;
    }
}

// Process Single Comment (Logic Core)
async function processComment(page, comment) {
    const { commenterName, commentUrl, commentText, connectionDegree, keyword, Row_ID, commentUrnId, forceReplyMessage } = comment;

    log(`Processing: ${commenterName} | Degree: ${connectionDegree} | Keyword: ${keyword ? 'Yes' : 'No'} | ID: ${commentUrnId}`);

    try {
        // 0. FORCE REPLY MODE (Used when Server calls back with AI Reply)
        if (forceReplyMessage) {
            log(`🚀 Force Reply Mode Activated. Posting provided message...`);
            const success = await postReply(page, commentUrl, forceReplyMessage, commentUrnId);
            return {
                status: success ? 'success' : 'failed',
                action: 'AI_REPLY_POSTED',
                message: forceReplyMessage,
                connectionStatus: connectionDegree
            };
        }

        // 1. Extract Rich Data
        const rootPostData = await extractRootPostData(page);

        // Build Rich Payload
        const richPayload = {
            action_type: 'reply',
            root_post_id: rootPostData ? rootPostData.root_post_id : '',
            root_post_author: rootPostData ? rootPostData.root_post_author : { name: 'Unknown' },
            post_text: rootPostData ? rootPostData.post_text : '',
            post_engagement_numbers: rootPostData ? rootPostData.post_engagement_numbers : {},
            comment_text: commentText, // The comment we are replying to
            commenter_name: commenterName,
            timestamp: new Date().toISOString(),
            locale: 'en-US'
        };

        let message = '';
        let action = '';

        // LOGIC TREE
        if (!keyword) {
            // Case 2: No Keyword -> AI Reply
            action = 'AI_REPLY';
            // We return the RICH PAYLOAD so server.js can call the webhook
            log(`Action: AI Reply (No Keyword) - Returning Rich Payload`);
            return {
                status: 'ai_reply_needed',
                payload: richPayload,
                commentUrl,
                commentUrnId
            };
        } else {
            // Keyword Present
            if (connectionDegree === '1st') {
                // Case 3: Connected + Keyword -> Skip
                action = 'SKIP';
                log('Action: SKIP (Connected + Keyword -> DM Workflow)');
                return {
                    status: 'skipped',
                    reason: 'Connected + Keyword',
                    connectionStatus: connectionDegree
                };
            } else {
                // Case 1: Not Connected + Keyword -> Reply to Connect
                action = 'REPLY_CONNECT';
                message = CONFIG.MESSAGES.CONNECT_REQUEST;
                log('Action: Reply to Connect (Not Connected + Keyword)');

                // Post immediately since we have the message
                const success = await postReply(page, commentUrl, message, commentUrnId);
                return {
                    status: success ? 'success' : 'failed',
                    action,
                    message,
                    connectionStatus: connectionDegree
                };
            }
        }

    } catch (error) {
        log(`Error: ${error.message}`, 'ERROR');
        return { status: 'error', error: error.message };
    }
}

// Global Browser
let globalBrowser = null;
let globalContext = null;

async function processSingleComment(commentData) {
    if (!globalBrowser) {
        globalBrowser = await chromium.launch({ headless: CONFIG.HEADLESS, slowMo: CONFIG.SLOW_MO });
        const contextOptions = { viewport: { width: 1920, height: 1080 } };
        if (fs.existsSync(CONFIG.SESSION_FILE)) {
            contextOptions.storageState = JSON.parse(fs.readFileSync(CONFIG.SESSION_FILE, 'utf-8'));
        }
        globalContext = await globalBrowser.newContext(contextOptions);
    }

    const page = await globalContext.newPage();
    try {
        return await processComment(page, commentData);
    } finally {
        await page.close();
    }
}

// Export for server.js AND internal use
module.exports = { processSingleComment, postReply };
