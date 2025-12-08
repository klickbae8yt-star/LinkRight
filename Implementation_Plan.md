# Implementation Plan - LinkedIn Reply Automation

## Goal Description
Automate LinkedIn comment replies based on connection status and lead keywords. The system will run locally, triggered by an HTTP request (e.g., from n8n), and use browser automation to post replies.

## User Review Required
> [!IMPORTANT]
> **Command+B vs Command+V**: You mentioned `Command+B` to paste. Usually, `Command+V` is paste. I will assume you mean **Paste** and use the appropriate simulation.
> **Logic Priority**:
> 1. **Keyword + Not Connected** → **Reply**: "Please connect so I can send [Resource]".
> 2. **No Keyword (Any Status)** → **AI Reply**: Fetch from Webhook & Post.
> 3. **Keyword + Connected** → **Skip** (Handled in future DM workflow).

## Proposed Changes

### Execution Layer
#### [NEW] [server.js](file:///Users/satvikjain/Documents/Miraya%20Lead%20Magnet/execution/server.js)
- A simple Express.js server running on a local port (e.g., 3000).
- Endpoint: `POST /reply`
- Accepts JSON body: `{ "commentUrl": "...", "connectionDegree": "...", "keyword": "...", "rowId": "..." }`
- Triggers `linkedin_reply_automation.js`.

#### [MODIFY] [linkedin_reply_automation.js](file:///Users/satvikjain/Documents/Miraya%20Lead%20Magnet/execution/linkedin_reply_automation.js)
- **Remove**: Redundant `checkConnectionStatus` (use input `Connection_Degree`).
- **Update `processComment`**:
    - Check `Connection_Degree`.
    - If `!= 1st`: Use "Not Connected" template.
    - If `== 1st` AND `!Keyword`: Call `https://n8n.link/LinkedIn reply` (mock/real) to get AI text.
    - If `== 1st` AND `Keyword`: Log "Skipped for DM workflow".
- **Refine `postReply`**: Ensure `Shift+Tab` navigation matches the user's specific request.

## Verification Plan

### Automated Tests
- **Test Server**: Run `node execution/server.js` and send a curl request.
- **Test Automation**: Use a dummy LinkedIn post (or the user's active session) to verify the `Shift+Tab` navigation works.

### Manual Verification
1.  Run the server.
2.  Send a test payload via Postman/Curl.
3.  Watch the browser (non-headless) navigate, find the reply button, and paste the text.
