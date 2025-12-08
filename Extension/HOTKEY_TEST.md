# Command+Shift+. (Period) Hotkey - Debug Test

## Changes Applied

1. **Added toggle debounce** - Prevents rapid ON/OFF/ON toggling
2. **Fixed UI update** - Updates UI elements directly without full re-render
3. **Added comprehensive logging** - Logs every step of the hotkey flow
4. **Added test hotkey** - Cmd+Shift+T to verify event listener is working

## Test Steps

### Step 1: Reload Extension

1. Go to `chrome://extensions`
2. Find "LinkRight"
3. Click reload button (⟳)

### Step 2: Reload LinkedIn

1. Go back to LinkedIn
2. Press Command+R (or F5) to refresh
3. Wait for page to fully load

### Step 3: Open Console

1. Press F12 or Command+Option+I
2. Go to Console tab
3. Clear console (click 🚫 icon or Cmd+K)

### Step 4: Check Initialization

Look for these logs:

```
LinkRight: Widget initialized and exposed to window.linkrightWidget
LinkRight: Hotkey listener registered (Cmd+Shift+. or Ctrl+Shift+.)
```

If you DON'T see these, the extension didn't load. Reload again.

### Step 5: Test Event Listener

Press **Command+Shift+T** (anywhere on the page)

**Expected**: You should see:

```
LinkRight: TEST - Cmd+Shift+T detected! Event listener is working.
```

**If you see this**, the event listener IS working and ready.
**If you DON'T see this**, the listener didn't attach - report this.

### Step 6: Enable Engagement Mode

1. Click the LinkRight "LR" icon
2. Click "Smart Engagement" button
3. You should see:
   - Toast: "✅ Smart Engagement enabled"
   - Console: `LinkRight: Engagement mode toggled to: true`
   - Console: `Starting LinkedIn monitoring...`
   - **NO rapid toggling!**

### Step 7: Test the Hotkey

1. Click "Comment" on any LinkedIn post
2. **IMPORTANT**: Click INSIDE the comment editor box (cursor must be blinking)
3. **Keep Console visible**
4. Press **Command+Shift+L** (Mac) or **Ctrl+Shift+L** (Windows)

## Expected Results

### If Everything Works

You'll see this sequence in console:

```
LinkRight: Cmd/Ctrl+Shift key detected { key: "l", code: "KeyL", ... }
LinkRight: Cmd+Shift+L detected { engagementMode: true, activeElement: "DIV", isEditor: true }
LinkRight: Processing hotkey...
LinkRight: Starting hotkey flow
LinkRight: Editor found { tag: "DIV", classes: "ql-editor..." }
LinkRight: Post data extracted { textLength: 145, actionType: "comment" }
LinkRight: Calling webhook...
LinkRight: Sending to webhook { url: "https://n8n.linkright.in/webhook/linkedin-reply", ... }
Extracted post text: ...
LinkRight: Webhook response { status: 200, ok: true }
LinkRight: Webhook result { hasComment: true, commentLength: 62 }
LinkRight: AI comment generated, pasting...
```

### If Engagement Mode is OFF

You'll see:

```
LinkRight: Cmd/Ctrl+Shift key detected { key: "l", ... }
LinkRight: Cmd+Shift+L detected { engagementMode: false, ... }
LinkRight: Hotkey blocked - engagement mode is OFF
```

Toast: "Turn on Smart Engagement first"

### If Not in Editor

You'll see:

```
LinkRight: Cmd/Ctrl+Shift key detected { key: "l", ... }
LinkRight: Cmd+Shift+L detected { engagementMode: true, activeElement: "BODY", isEditor: false }
LinkRight: Hotkey blocked - not in editor { element: "BODY", ... }
```

Toast: "Click inside comment editor first"

### If Event Listener Isn't Working

You'll see:

- **NOTHING** - no logs at all

In this case, the problem is that the event listener didn't attach properly.

## Troubleshooting

### Problem: No logs when pressing Cmd+Shift+T

**Cause**: Event listener not attached
**Fix**:

- Check if extension is enabled
- Reload extension
- Hard refresh LinkedIn (Cmd+Shift+R)
- Check for JavaScript errors preventing script execution

### Problem: "Cmd/Ctrl+Shift key detected" shows but wrong key

**Cause**: You pressed a different key
**Fix**: Make sure you press L (lowercase L, not I or 1)

### Problem: Shows "engagementMode: false"

**Cause**: Smart Engagement is OFF
**Fix**: Click the "Smart Engagement" button first

### Problem: Shows "isEditor: false"

**Cause**: Cursor is not in the comment box
**Fix**: Click inside the comment editor, make sure cursor is blinking

## Report Back

After testing, share:

1. Did you see the initialization logs?
2. Did Cmd+Shift+T work?
3. What happened when you pressed Cmd+Shift+L?
4. Copy ALL console logs that appeared
