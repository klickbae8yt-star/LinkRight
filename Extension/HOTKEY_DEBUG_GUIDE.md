# Command+Shift+. Hotkey Debug Guide

## What Was Fixed

### 1. **Added Debug Logging**

The hotkey handler now logs detailed information at every step:

- When the key combination is detected
- Current engagement mode status
- Active element details
- Editor detection results
- Webhook calls and responses

### 2. **Improved Error Messages**

Added helpful toast notifications:

- "Turn on Smart Engagement first" - if engagement mode is OFF
- "Click inside comment editor first" - if cursor is not in the editor
- Existing error messages for webhook failures

### 3. **Exposed Widget for Debugging**

The widget is now accessible via `window.linkrightWidget` for console debugging.

### 4. **Added Webhook Logging**

Every webhook call now logs:

- Request details (URL, data keys)
- Response status
- Result content

## How to Test

### Step 1: Reload the Extension

1. Go to `chrome://extensions`
2. Find "LinkRight" extension
3. Click the reload icon (⟳)
4. Go back to LinkedIn

### Step 2: Verify Widget is Loaded

Open Chrome DevTools Console (F12) and check for:

```
LinkRight: Widget initialized and exposed to window.linkrightWidget
LinkRight: Hotkey listener registered (Cmd+Shift+. or Ctrl+Shift+.)
```

### Step 3: Enable Engagement Mode

1. Click the LinkRight icon in LinkedIn
2. Click the "Smart Engagement" button
3. Verify in console: `LinkRight: Updating UI state, engagement mode: true`
4. Verify monitoring starts: `Starting LinkedIn monitoring...`

### Step 4: Test the Hotkey

1. **Open a comment box**: Click "Comment" on any LinkedIn post
2. **Click inside the editor**: Make sure the cursor is blinking in the comment box
3. **Press Command+Shift+.** (period) on Mac or **Ctrl+Shift+.** on Windows

### Expected Console Output

When you press the hotkey, you should see:

```javascript
LinkRight: Cmd+Shift+L detected {
  engagementMode: true,
  activeElement: "DIV",
  isEditor: true
}
LinkRight: Processing hotkey...
LinkRight: Starting hotkey flow
LinkRight: Editor found { tag: "DIV", classes: "ql-editor..." }
LinkRight: Post data extracted { textLength: 145, actionType: "comment" }
LinkRight: Calling webhook...
LinkRight: Sending to webhook { url: "https://...", dataKeys: [...] }
LinkRight: Webhook response { status: 200, ok: true }
LinkRight: Webhook result { hasComment: true, commentLength: 85 }
LinkRight: Got response { hasComment: true }
LinkRight: AI comment generated, pasting...
```

## Troubleshooting

### Issue 1: "Cmd+Shift+L detected" doesn't appear

**Problem**: The event listener isn't working
**Solution**:

- Reload the extension
- Reload the LinkedIn page
- Check if another extension is capturing the hotkey

### Issue 2: "engagementMode: false" appears

**Problem**: Engagement mode is not enabled
**Solution**:

- Click the "Smart Engagement" button in the sidebar
- Verify the button shows as active (golden border)

### Issue 3: "isEditor: false" appears

**Problem**: The cursor is not in a comment editor
**Solution**:

- Click inside the comment box so the cursor is blinking
- Make sure you're in a `.ql-editor` element

### Issue 4: "LinkRight: Hotkey blocked - not in editor"

**Problem**: Focus detection issue
**Solution**: Run this in console to debug:

```javascript
// Click in the editor first, then run:
console.log({
  activeElement: document.activeElement,
  tag: document.activeElement.tagName,
  contenteditable: document.activeElement.getAttribute("contenteditable"),
  classes: Array.from(document.activeElement.classList),
  isEditor: window.linkrightWidget.isEditorElement(document.activeElement),
});
```

### Issue 5: Webhook errors

**Problem**: Network or CORS issues
**Solution**: Check the Network tab in DevTools:

- Look for requests to `n8n.linkright.in`
- Check response status and errors
- Verify CORS headers if needed

## Quick Console Commands

```javascript
// Check engagement mode
window.linkrightWidget.engagementMode;

// Check active element
document.activeElement;

// Check if current element is an editor
window.linkrightWidget.isEditorElement(document.activeElement);

// Manually trigger the hotkey handler
window.linkrightWidget.handleHotkeyGeneratePasteSubmit(document.activeElement);

// Check webhook URL
window.LINKRIGHT_CONFIG.WEBHOOK_URL;
```

## Next Steps

After testing, if the issue persists:

1. Copy the complete console output
2. Note which step fails
3. Check the Network tab for webhook requests
4. Share the logs for further debugging
