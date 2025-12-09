# LinkRight - Complete Documentation

## Overview

LinkedIn Lead Magnet automation tool with Chrome Extension for:
- Comment scraping with keyword filtering
- Smart Engagement (AI-powered replies)
- Reply Automation (Playwright-based)
- DM Workflow (upcoming)

---

## Architecture

### 3-Layer System
| Layer | Location | Purpose |
|-------|----------|---------|
| **Directives** | `directives/` | SOPs in Markdown |
| **Orchestration** | AI Agent | Decision-making & routing |
| **Execution** | `execution/` | Deterministic Node.js/Playwright scripts |

---

## Quick Start

### 1. Install Dependencies
```bash
cd "/Users/satvikjain/Documents/Miraya Lead Magnet"
npm install
npm run install-browsers
```

### 2. Load Chrome Extension
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select `Extension/` folder

### 3. Start Backend Server
```bash
node execution/server.js
```
Server runs on `http://localhost:3000`

### 4. First-time LinkedIn Login
```bash
node execution/linkedin_reply_automation.js
```
- Login manually in the browser
- Session saved to `linkedin_session.json`

---

## Extension Features

### Sidebar UI Buttons
| Button | Action |
|--------|--------|
| Expand Comments | Clicks all "Show more" buttons |
| Scrape Console | Extracts comments → Clipboard + Webhook |
| Categorize Leads | Triggers n8n categorization workflow |
| Start Reply Automation | Triggers Playwright reply loop |
| Smart Engagement Toggle | Enables AI reply on Cmd+Shift+. |

### Default Settings
| Setting | Default Value |
|---------|---------------|
| Webhook Collect Comments | `https://n8n.linkright.in/webhook/collect-comments` |
| Webhook Lead Categorization | `https://n8n.linkright.in/webhook/lead-categorization` |
| Webhook AI Reply | `https://n8n.linkright.in/webhook/linkedin-reply` |
| Google Sheets ID | `19ziyAH5xJeAF8fW4Kb31gzrv0_Lluiuw9NGGan6xIKc` |
| Lead Gen Keywords | `DM` |
| Backend URL | `http://127.0.0.1:3000` |

---

## Google Sheets Structure

Required columns in `Comments_Master`:

| Column | Name | Description |
|--------|------|-------------|
| A | Row_ID | Unique ID (auto-generated) |
| B | Timestamp_Captured | When scraped |
| C | Post_URL | LinkedIn post URL |
| E | Commenter_Name | Full name |
| F | Commenter_Profile_URL | LinkedIn profile URL |
| H | Comment_Text | Comment content |
| I | Comment_URL | Comment permalink |
| N | Connection_Degree | 1st/2nd/3rd/None |
| O | Processing_Status | Categorized → Delivered |
| P | Comment_Reply_Sent | Yes/No |

### Row ID Formula (A2)
```excel
=ARRAYFORMULA(IF(ISBLANK(B2:B), "", ROW(A2:A)-1))
```

---

## Backend API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/process-single-comment` | POST | n8n calls this to trigger Playwright |
| `/api/reply-automation/start` | POST | Extension calls this to start automation |

---

## Workflow Diagrams

### Comment Scraping Flow
```
LinkedIn Post → Expand Comments → Scrape Console
    ↓
Extension extracts: Name, Profile, Comment, URL, Connection
    ↓
Data → Clipboard (CSV) + Webhook (JSON)
    ↓
n8n → Google Sheets
```

### Reply Automation Flow
```
n8n reads Google Sheets (Processing_Status = "Categorized")
    ↓
For each comment:
├─ HTTP POST to localhost:3000/process-single-comment
├─ Playwright opens browser with saved session
├─ Navigate to Comment_URL
├─ Shift+Tab → Enter → Paste Reply → Tab×3 → Enter
├─ Update Sheet (Status = "Delivered")
└─ Wait 8-15 seconds
```

---

## Troubleshooting

### Session Expired
```bash
rm linkedin_session.json
node execution/linkedin_reply_automation.js
# Login manually
```

### Extension Not Working
1. Reload extension in `chrome://extensions/`
2. Check console for errors
3. Verify server is running on port 3000

### CORS Errors
- Webhook calls → Routed through background.js (CORS bypass)
- Local server → Has CORS middleware enabled

---

## File Structure

```
Miraya Lead Magnet/
├── Extension/           # Chrome Extension
│   ├── manifest.json
│   ├── content.js       # Main logic
│   ├── background.js    # Webhook proxy
│   └── sidebar.css      # Styles
├── execution/           # Backend scripts
│   ├── server.js        # Express API
│   └── linkedin_reply_automation.js
├── templates/           # Google Sheets templates
├── directives/          # SOPs
└── README.md            # This file
```

---

## Recent Changes (Dec 2025)

| Change | Reason |
|--------|--------|
| CORS proxy in background.js | Webhook calls blocked by LinkedIn |
| Expand Comments fix | Exclude "Collapse" buttons |
| Port changed to 3000 | Match ngrok config |
| Default Google Sheets ID | Pre-configured for user |
| Lead Gen Keyword = "DM" | Default filter |

---

## Safety Notes

⚠️ **Rate Limits:**
- Max 25 replies per session
- 10-minute break between sessions

⚠️ **LinkedIn ToS:**
- Use responsibly
- Don't spam
- Respect connection requests

---

**Happy Automating!** 🚀
