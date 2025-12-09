/**
 * LinkedIn Reply Automation - Background Script
 * Handles settings, icon updates, and backend communication
 */

// Settings management
let settings = getDefaultSettings();

function getDefaultSettings() {
    return {
        // Webhooks (Production URLs - synced with content.js)
        webhookCollectComments: 'https://n8n.linkright.in/webhook/collect-comments',
        webhookLeadCategorization: 'https://n8n.linkright.in/webhook/lead-categorization',
        webhookAiReply: 'https://n8n.linkright.in/webhook/linkedin-reply',

        // Reply Automation
        googleSheetsId: '',

        // Message templates
        messageConnected: "Thanks for your interest! Sending you the resource via DM now. Check your messages! 📩",
        messageNotConnected: "Hey! We're not connected yet. Please send me a connection request and DM me with 'GEMINI' - I'll send you the resource right away! 🚀",
        messagePending: "Hey! I see you've sent a connection request. I'll accept it shortly and send you the resource via DM! 👍",

        // Backend
        backendUrl: 'http://127.0.0.1:3001'
    };
}

// Load settings on startup
chrome.runtime.onInstalled.addListener(async () => {
    console.log('LinkedIn Reply Extension installed');
    await loadSettings();
    updateIcon(false);
});

// Load settings from storage
async function loadSettings() {
    try {
        const result = await chrome.storage.local.get(['linkedin_reply_settings']);
        if (result.linkedin_reply_settings) {
            settings = { ...getDefaultSettings(), ...result.linkedin_reply_settings };
        }
    } catch (error) {
        console.error('Failed to load settings:', error);
    }
}

// Save settings to storage
async function saveSettings(newSettings) {
    try {
        settings = { ...settings, ...newSettings };
        await chrome.storage.local.set({ linkedin_reply_settings: settings });
        console.log('Settings saved');
    } catch (error) {
        console.error('Failed to save settings:', error);
    }
}

// Handle extension icon click
chrome.action.onClicked.addListener(async (tab) => {
    if (tab.url && tab.url.includes('linkedin.com')) {
        try {
            await chrome.tabs.sendMessage(tab.id, { type: 'OPEN_SIDEBAR' });
        } catch (error) {
            console.log('Content script not loaded, injecting...');
            await injectContentScript(tab.id);
            await chrome.tabs.sendMessage(tab.id, { type: 'OPEN_SIDEBAR' });
        }
    }
});

// Inject content script if not loaded
async function injectContentScript(tabId) {
    try {
        await chrome.scripting.insertCSS({
            target: { tabId },
            files: ['sidebar-simplified.css']
        });
        await chrome.scripting.executeScript({
            target: { tabId },
            files: ['content-simplified.js']
        });
    } catch (error) {
        console.error('Failed to inject content script:', error);
    }
}

// Handle messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'LOAD_SETTINGS') {
        sendResponse({ success: true, settings });
        return true;
    }

    if (message.type === 'SAVE_SETTINGS') {
        saveSettings(message.settings).then(() => {
            sendResponse({ success: true });
        });
        return true;
    }

    if (message.type === 'UPDATE_ICON') {
        updateIcon(message.active);
        sendResponse({ success: true });
        return true;
    }

    if (message.type === 'TRIGGER_LEAD_CATEGORIZATION') {
        fetch('https://n8n.linkright.in/webhook/lead-categorization')
            .then(response => {
                if (response.ok) {
                    sendResponse({ success: true });
                } else {
                    sendResponse({ success: false, error: 'Webhook failed: ' + response.status });
                }
            })
            .catch(error => {
                sendResponse({ success: false, error: error.message });
            });
        return true; // Keep channel open for async response
    }

    // Generic Webhook Proxy (CORS bypass)
    if (message.type === 'FETCH_WEBHOOK') {
        const { url, method, body } = message;
        console.log('🔄 Proxying webhook call:', url);

        fetch(url, {
            method: method || 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body ? JSON.stringify(body) : undefined
        })
            .then(async response => {
                if (!response.ok) {
                    throw new Error(`Webhook failed: ${response.status}`);
                }
                const data = await response.json().catch(() => ({}));
                console.log('✅ Webhook response:', data);
                sendResponse({ success: true, data });
            })
            .catch(error => {
                console.error('❌ Webhook error:', error);
                sendResponse({ success: false, error: error.message });
            });
        return true; // Keep channel open for async response
    }
});

// Update extension icon
function updateIcon(active) {
    const iconPath = active ? 'icons/icon48.png' : 'icons/icon48_gray.png';
    chrome.action.setIcon({
        path: {
            16: iconPath.replace('48', '16'),
            48: iconPath,
            128: iconPath.replace('48', '128')
        }
    });
}
