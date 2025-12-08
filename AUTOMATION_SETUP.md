# LinkedIn Reply Automation - Setup Guide

## Quick Start (Local Machine)

### Step 1: Install Dependencies

```bash
cd "/Users/satvikjain/Documents/Miraya Lead Magnet"
npm install
npm run install-browsers
```

### Step 2: First Run (Manual Login)

The first time you run the script, you'll need to log in to LinkedIn manually:

```bash
node execution/linkedin_reply_automation.js
```

**What happens:**
1. Browser opens (headed mode)
2. Navigate to LinkedIn and **log in manually**
3. Script will save your session to `linkedin_session.json`
4. Future runs will reuse this session (no login needed)

### Step 3: Prepare Your Comment Data

Edit the `sampleComments` array in `execution/linkedin_reply_automation.js` (line 260):

```javascript
const sampleComments = [
  {
    commenterName: "John Doe",
    commenterProfileUrl: "https://www.linkedin.com/in/johndoe",
    commentText: "GEMINI - this looks interesting!",
    commentUrl: "https://www.linkedin.com/feed/update/urn:li:activity:123?commentUrn=..."
  },
  // Add more comments from your Google Sheets
];
```

**Or** integrate with Google Sheets (see below).

### Step 4: Run Automation

```bash
node execution/linkedin_reply_automation.js
```

**Watch the magic happen:**
- Browser opens
- Checks each commenter's connection status
- Posts appropriate reply with @mention
- Logs everything to console
- Saves results to `automation_results.json`

---

## Features

✅ **Keyboard Navigation** - No DOM manipulation, pure user simulation
✅ **Auto @mention** - LinkedIn automatically tags the commenter
✅ **Connection Check** - Detects Connected/Pending/Not Connected
✅ **Smart Messages** - Different templates based on connection status
✅ **Human Delays** - Random 2-4 second delays between actions
✅ **Detailed Logging** - Color-coded console output with timestamps
✅ **Session Persistence** - Login once, reuse forever
✅ **Error Handling** - Graceful failures with detailed error logs

---

## Configuration

Edit `CONFIG` object in `execution/linkedin_reply_automation.js`:

```javascript
const CONFIG = {
  SESSION_FILE: './linkedin_session.json',
  HEADLESS: false,  // Set true to hide browser
  SLOW_MO: 100,     // Milliseconds between actions
  
  MESSAGES: {
    CONNECTED: "Your message here...",
    NOT_CONNECTED: "Your message here...",
    PENDING: "Your message here..."
  }
};
```

---

## Logging

The script provides detailed, color-coded logs:

- 🔵 **INFO** (Cyan) - General information
- 🟢 **SUCCESS** (Green) - Successful operations
- 🟡 **WARNING** (Yellow) - Non-critical issues
- 🔴 **ERROR** (Red) - Failures

Example output:
```
[2025-12-07T23:30:00.000Z] [INFO] Starting LinkedIn Reply Automation...
[2025-12-07T23:30:01.000Z] [INFO] Launching browser...
[2025-12-07T23:30:05.000Z] [SUCCESS] Profile page loaded
[2025-12-07T23:30:08.000Z] [SUCCESS] Status: CONNECTED (Message button found)
[2025-12-07T23:30:15.000Z] [SUCCESS] Reply posted successfully!
```

---

## Human-Like Delays

All delays are randomized for natural behavior:

| Action | Delay Range |
|--------|-------------|
| Profile reading | 2-3 seconds |
| Auto-focus wait | 5-6 seconds |
| Keyboard press | 200-400ms |
| Reply box open | 800-1200ms |
| Message review | 1.5-2.5 seconds |
| Post confirmation | 2-3 seconds |
| Between comments | 8-15 seconds |

---

## Output

Results are saved to `automation_results.json`:

```json
[
  {
    "commenterName": "John Doe",
    "commenterProfileUrl": "https://linkedin.com/in/johndoe",
    "commentText": "GEMINI - this looks interesting!",
    "commentUrl": "https://linkedin.com/feed/update/...",
    "success": true,
    "connectionStatus": "CONNECTED",
    "message": "Thanks for your interest! Sending you the resource via DM now...",
    "timestamp": "2025-12-07T23:30:15.000Z"
  }
]
```

---

## Troubleshooting

### Session Expired
```bash
# Delete saved session and log in again
rm linkedin_session.json
node execution/linkedin_reply_automation.js
```

### Browser Not Opening
```bash
# Reinstall Playwright browsers
npm run install-browsers
```

### Script Hangs
- Check if LinkedIn page structure changed
- Verify comment URLs are correct
- Ensure internet connection is stable

---

## Next Steps

1. **Test with 1-2 comments** first
2. **Verify replies are posted correctly**
3. **Check connection status detection**
4. **Integrate with Google Sheets** (see below)
5. **Deploy to AWS EC2** (when ready)

---

## Google Sheets Integration (Coming Soon)

To integrate with your Google Sheets:

1. Install Google Sheets API library
2. Read comments from `Comments_Master` sheet
3. Filter rows where `Processing_Status = "Categorized"`
4. Pass to automation script
5. Update sheet with results

---

## Safety Notes

⚠️ **Rate Limits:**
- Max 25 replies per session
- 10-minute break between sessions
- Don't run 24/7

⚠️ **LinkedIn ToS:**
- This is automation - use responsibly
- Don't spam
- Respect connection requests

---

## Support

For issues or questions, check:
- Console logs (detailed error messages)
- `automation_results.json` (success/failure data)
- Screenshots (if enabled)

---

**Happy Automating!** 🚀
