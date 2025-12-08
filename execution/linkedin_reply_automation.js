/**
 * LinkedIn Comment Reply Automation
 * 
 * Features:
 * - Logic based on Connection Degree & Keywords
 * - Exact Keyboard Navigation (User Defined)
 * - AI Reply generation via Webhook
 * - Local Server Trigger
 */

const { chromium } = require('playwright');
const fs = require('fs');
const axios = require('axios');
// const { updateRow } = require('./google_sheets_client'); // Removed: n8n handles updates

// Configuration
const CONFIG = {
    SESSION_FILE: './execution/linkedin_session.json',
    HEADLESS: false,
    SLOW_MO: 100,
    // SHEET_ID: '19ziyAH5xJeAF8fW4Kb31gzrv0_Lluiuw9NGGan6xIKc', // Removed
    WEBHOOK_URL: 'https://n8n.link/LinkedIn-reply', // Placeholder - Update if needed

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

// Get AI Reply from Webhook
async function getAIReply(commentText) {
    log('Fetching AI reply from webhook...');
    try {
        // Mocking the call for now as URL might be incorrect
        // const response = await axios.post(CONFIG.WEBHOOK_URL, { comment: commentText });
        // return response.data.reply;

        // Fallback/Mock
        return "Thanks for your comment! (AI Generated)";
    } catch (error) {
        log(`Error fetching AI reply: ${error.message}`, 'ERROR');
        return "Thanks for sharing your thoughts!"; // Fallback
    }
}

// Post reply using Smart Tabbing with ID Verification
async function postReply(page, commentUrl, message, commentUrnId) {
    log(`Posting reply to: ${commentUrl} | ID: ${commentUrnId}`);

    try {
        await page.goto(commentUrl, { waitUntil: 'domcontentloaded' });
        log('Page loaded, waiting for scroll...');
        await sleep(randomDelay(5000, 8000));

        // Focus on the page body first
        await page.click('body');

        // Smart Tabbing Logic
        log('Starting Smart Tabbing to find correct Reply button...');
        let foundReply = false;
        let attempts = 0;
        const maxAttempts = 40; // Allow enough tabs to reach the comment

        while (!foundReply && attempts < maxAttempts) {
            await page.keyboard.press('Tab'); // Move forward
            await sleep(300); // Fast tab
            attempts++;

            // Check focused element
            const isTargetReplyButton = await page.evaluate((targetId) => {
                const active = document.activeElement;
                if (!active) return false;

                // Check if it's a Reply button
                const isReply = active.innerText.trim().toLowerCase() === 'reply' ||
                    (active.getAttribute('aria-label') && active.getAttribute('aria-label').toLowerCase().includes('reply'));

                if (!isReply) return false;

                // CRITICAL: Check if it belongs to our Target Comment ID
                const parentArticle = active.closest(`article[data-id="${targetId}"]`);
                return !!parentArticle; // True only if inside our specific comment
            }, commentUrnId);

            if (isTargetReplyButton) {
                foundReply = true;
                log(`✅ Target Reply button found and focused! (Attempt ${attempts})`);
            }
        }

        if (!foundReply) {
            log('⚠️ Could not find target via Tab. Trying Shift+Tab fallback...', 'WARN');
            // Fallback: Try Shift+Tab a few times if we overshot
            attempts = 0;
            while (!foundReply && attempts < 10) {
                await page.keyboard.press('Shift+Tab');
                await sleep(500);
                attempts++;

                const isTargetReplyButton = await page.evaluate((targetId) => {
                    const active = document.activeElement;
                    if (!active) return false;
                    const isReply = active.innerText.trim().toLowerCase() === 'reply' ||
                        (active.getAttribute('aria-label') && active.getAttribute('aria-label').toLowerCase().includes('reply'));
                    if (!isReply) return false;
                    return !!active.closest(`article[data-id="${targetId}"]`);
                }, commentUrnId);

                if (isTargetReplyButton) {
                    foundReply = true;
                    log(`✅ Target Reply button found via fallback!`);
                }
            }
        }

        if (!foundReply) {
            throw new Error('Could not find correct Reply button (ID mismatch or not found)');
        }

        // Open Reply Box
        await page.keyboard.press('Enter');
        await sleep(randomDelay(1500, 2500));

        // Paste Message
        log(`Pasting message...`);
        await page.evaluate((text) => {
            navigator.clipboard.writeText(text);
        }, message);

        await page.keyboard.press('Meta+V'); // Command+V
        await sleep(randomDelay(2000, 3000));

        // Tab 3 times to Post
        log('Pressing Tab (3x) to reach Post button...');
        await page.keyboard.press('Tab');
        await sleep(500);
        await page.keyboard.press('Tab');
        await sleep(500);
        await page.keyboard.press('Tab');
        await sleep(500);

        // Enter to Post
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
    const { commenterName, commentUrl, commentText, connectionDegree, keyword, Row_ID, commentUrnId } = comment;

    log(`Processing: ${commenterName} | Degree: ${connectionDegree} | Keyword: ${keyword ? 'Yes' : 'No'} | ID: ${commentUrnId}`);

    try {
        let message = '';
        let action = '';

        // LOGIC TREE
        if (!keyword) {
            // Case 2: No Keyword -> AI Reply
            action = 'AI_REPLY';
            message = await getAIReply(commentText);
            log(`Action: AI Reply (No Keyword)`);
        } else {
            // Keyword Present
            if (connectionDegree === '1st') {
                // Case 3: Connected + Keyword -> Skip
                action = 'SKIP';
                log('Action: SKIP (Connected + Keyword -> DM Workflow)');
                return {
                    status: 'skipped',
                    reason: 'Connected + Keyword',
                    message: '',
                    connectionStatus: connectionDegree
                };
            } else {
                // Case 1: Not Connected + Keyword -> Reply to Connect
                action = 'REPLY_CONNECT';
                message = CONFIG.MESSAGES.CONNECT_REQUEST;
                log('Action: Reply to Connect (Not Connected + Keyword)');
            }
        }

        // Execute Reply
        if (action === 'AI_REPLY' || action === 'REPLY_CONNECT') {
            const success = await postReply(page, commentUrl, message, commentUrnId);

            // Return result to n8n (Do NOT update sheet here)
            return {
                status: success ? 'success' : 'failed',
                action,
                message: message, // Return message so n8n can update sheet
                connectionStatus: connectionDegree
            };
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

module.exports = { processSingleComment };
