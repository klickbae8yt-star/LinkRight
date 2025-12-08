# LinkedIn Reply Automation - Setup Guide

## 🚀 Quick Start

This simplified Chrome Extension automates LinkedIn comment replies using Google Sheets integration and Playwright.

---

## 📋 Prerequisites

1. **Node.js** (v16+)
2. **Google Cloud Project** with Sheets API enabled
3. **Chrome Browser**
4. **LinkedIn Account**

---

## 🔧 Installation

### **Step 1: Install Dependencies**

```bash
cd "/Users/satvikjain/Documents/Miraya Lead Magnet"
npm install
npm run install-browsers
```

### **Step 2: Google Sheets API Setup**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable **Google Sheets API**
4. Create **OAuth 2.0 Client ID** (Desktop app)
5. Download credentials as `credentials.json`
6. Place in project root: `/Users/satvikjain/Documents/Miraya Lead Magnet/credentials.json`

### **Step 3: First-time OAuth**

```bash
# Run this once to generate token.json
node execution/authenticate_google.js
```

Follow browser prompts to authorize. This creates `token.json`.

### **Step 4: Load Chrome Extension**

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select folder: `/Users/satvikjain/Documents/Miraya Lead Magnet/Extension`
5. **Important:** Use the simplified files:
   - Rename `manifest-simplified.json` → `manifest.json`
   - Rename `content-simplified.js` → `content.js`
   - Rename `background-simplified.js` → `background.js`
   - Rename `sidebar-simplified.css` → `sidebar.css`

### **Step 5: Start Backend Server**

```bash
npm start
```

Server runs on `http://localhost:3001`

---

## ⚙️ Configuration

### **Extension Settings**

1. Open LinkedIn
2. Click extension icon
3. Open Settings (collapsible section)
4. Configure:
   - **Smart Engagement Webhook:** `https://n8n.linkright.in/webhook/linkedin-reply`
   - **Google Sheets ID:** Your sheet ID (from URL)
   - **Backend URL:** `http://127.0.0.1:3001`
   - **Message Templates:** Customize for Connected/Not Connected/Pending

### **Google Sheets Structure**

Your `Comments_Master` sheet must have these columns:

| Column | Name | Description |
|--------|------|-------------|
| A | Row_ID | Unique ID |
| E | Commenter_Name | Name |
| F | Commenter_Profile_URL | Profile URL |
| H | Comment_Text | Comment text |
| I | Comment_URL | Comment URL (with commentUrn & dashCommentUrn) |
| N | Connection_Status | CONNECTED/NOT_CONNECTED/PENDING |
| O | Processing_Status | **Categorized** (to process) → **Delivered** (done) |
| P | Comment_Reply_Sent | Yes/No |
| Q | Comment_Reply_Text | Reply message |
| R | Comment_Reply_Timestamp | When replied |

---

## 🎯 Usage

### **Smart Engagement (Manual AI Comments)**

1. Enable toggle in extension
2. Click comment button on any LinkedIn post
3. AI-generated comment appears automatically
4. Review and post manually

### **Reply Automation (Automated)**

1. Prepare Google Sheets:
   - Add comment URLs
   - Set `Processing_Status = "Categorized"`
2. Click "Start Reply Automation" in extension
3. Automation:
   - Reads categorized comments
   - Opens Chromium browser
   - Checks connection status
   - Posts replies with @mention
   - Updates Google Sheets
   - Processes all comments sequentially

---

## 🔐 Session Management

**First Run:**
- Browser opens
- Manual LinkedIn login required
- Session saved to `linkedin_session.json`

**Subsequent Runs:**
- Auto-login using saved session
- No manual intervention needed

---

## 📊 Monitoring

**Backend Logs:**
```bash
# Terminal shows real-time progress
Processing comment 1/10
Commenter: John Doe
Connection status: CONNECTED
Reply posted successfully
Waiting 12000ms before next comment...
```

**Extension UI:**
- Progress bar shows current/total
- Status text updates in real-time
- Completion summary displayed

---

## 🐛 Troubleshooting

### **Extension Not Loading**
```bash
# Check if files are renamed correctly
ls Extension/manifest.json
ls Extension/content.js
ls Extension/background.js
ls Extension/sidebar.css
```

### **Backend Connection Failed**
```bash
# Verify server is running
curl http://localhost:3001/health
# Should return: {"status":"ok","running":false}
```

### **Google Sheets Authentication Error**
```bash
# Re-run OAuth flow
rm token.json
node execution/authenticate_google.js
```

### **LinkedIn Session Expired**
```bash
# Delete session and re-login
rm linkedin_session.json
# Next automation run will prompt for login
```

---

## 📁 File Structure

```
Miraya Lead Magnet/
├── Extension/
│   ├── manifest.json (simplified)
│   ├── content.js (simplified - 550 lines)
│   ├── background.js (simplified - 100 lines)
│   ├── sidebar.css (simplified - 250 lines)
│   └── icons/
├── execution/
│   ├── server.js (Express API)
│   ├── google_sheets_client.js (Sheets integration)
│   └── linkedin_reply_automation.js (original standalone)
├── credentials.json (Google OAuth)
├── token.json (Generated after auth)
├── linkedin_session.json (LinkedIn cookies)
└── package.json
```

---

## 🔄 Workflow Diagram

```
User clicks "Start Reply Automation"
  ↓
Extension → POST /api/reply-automation/start
  ↓
Backend reads Google Sheets (Processing_Status = "Categorized")
  ↓
For each comment:
  ├─ Open Chromium (saved session)
  ├─ Navigate to Commenter_Profile_URL
  ├─ Check connection (Message/Connect/Pending button)
  ├─ Navigate to Comment_URL
  ├─ Keyboard navigation: Shift+Tab → Enter → Paste → Tab×3 → Enter
  ├─ Update Google Sheets (Status = "Delivered")
  └─ Wait 8-15 seconds (human delay)
  ↓
Automation complete
```

---

## ✅ Success Checklist

- [ ] Dependencies installed (`npm install`)
- [ ] Chromium installed (`npm run install-browsers`)
- [ ] `credentials.json` in project root
- [ ] `token.json` generated (OAuth complete)
- [ ] Extension loaded in Chrome (simplified files)
- [ ] Backend server running (`npm start`)
- [ ] Google Sheets ID configured in extension
- [ ] Test comment added to sheet (Processing_Status = "Categorized")
- [ ] Manual LinkedIn login completed (first run)
- [ ] Test automation successful

---

## 🎉 You're Ready!

Extension is now 71% smaller (2,750 lines vs 9,634 original) and focused exclusively on comment reply automation.

**Next Steps:**
1. Add test comments to Google Sheets
2. Run automation
3. Verify replies posted
4. Check Google Sheets updated

**Support:** Check logs in terminal for detailed debugging info.
