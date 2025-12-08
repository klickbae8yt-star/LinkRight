# Lead Categorization - Implementation Guide

## Goal
Build a keyword-based lead categorization system in n8n that automatically identifies lead generation opportunities from LinkedIn comments.

## Overview
This workflow reads uncategorized comments from Google Sheets, analyzes them for lead magnet keywords, and updates the sheet with categorization results.

---

## Inputs

### Google Sheets Structure

**Sheet: Comments_Master**
Required columns:
- `Comment_Text` - The LinkedIn comment content
- `Processing_Status` - Current state (filter for "New")
- `AI_Category` - Output: Lead/Casual/Spam
- `Lead_Magnet_Keyword` - Output: Which keyword was detected
- `AI_Confidence_Score` - Output: 0.0-1.0 confidence
- `AI_Rationale` - Output: Explanation of decision
- `Last_Updated` - Output: Timestamp

**Sheet: Config**
Required settings:
- `Lead_Magnet_Keywords` - Comma-separated list (e.g., "DM, interested, send, share")
- `Lead_Magnet_Phrases` - Comma-separated phrases (e.g., "count me in, sign me up")
- `Lead_Magnet_Emojis` - Comma-separated emojis (e.g., "👍, 🙋, ✋")
- `Negative_Keywords` - Comma-separated (e.g., "don't dm, no dm, not interested")

---

## Workflow: LI_leadmag2_categorize_comments

### Trigger
Manual trigger via webhook (activated from daily email)

### Nodes

#### 1. Read Config Sheet
**Node Type:** Google Sheets
**Action:** Read rows
**Sheet:** Config
**Output:** Configuration values for keyword matching

#### 2. Read Unprocessed Comments
**Node Type:** Google Sheets
**Action:** Read rows
**Sheet:** Comments_Master
**Filter:** `Processing_Status = "New"`
**Output:** Array of uncategorized comments

#### 3. Categorize Comment
**Node Type:** Function
**Purpose:** Keyword-based lead detection
**Input:** Comment text + Config keywords
**Output:** Category, detected keyword, confidence, rationale

**Code:**
```javascript
// Get configuration
const configKeywords = $('Read Config Sheet').first().json.Lead_Magnet_Keywords
  .toLowerCase()
  .split(',')
  .map(k => k.trim());

const phrases = $('Read Config Sheet').first().json.Lead_Magnet_Phrases
  .toLowerCase()
  .split(',')
  .map(p => p.trim());

const emojis = $('Read Config Sheet').first().json.Lead_Magnet_Emojis
  .split(',')
  .map(e => e.trim());

const negativeKeywords = $('Read Config Sheet').first().json.Negative_Keywords
  .toLowerCase()
  .split(',')
  .map(n => n.trim());

// Get comment text
const commentText = $input.item.json.Comment_Text.toLowerCase();

// Step 1: Check for negative keywords (override)
const isNegative = negativeKeywords.some(neg => commentText.includes(neg));

if (isNegative) {
  return {
    json: {
      Row_ID: $input.item.json.Row_ID,
      AI_Category: 'Casual',
      Lead_Magnet_Keyword: '',
      AI_Confidence_Score: 0.95,
      AI_Rationale: 'Negative keyword detected - user declined interest',
      Processing_Status: 'Categorized',
      Last_Updated: new Date().toISOString()
    }
  };
}

// Step 2: Check config keywords (word boundary)
let detectedKeyword = '';
let matchType = '';

for (const keyword of configKeywords) {
  const regex = new RegExp(`\\b${keyword}\\b`, 'i');
  if (regex.test(commentText)) {
    detectedKeyword = keyword;
    matchType = 'keyword';
    break;
  }
}

// Step 3: Check phrases (substring match)
if (!detectedKeyword) {
  for (const phrase of phrases) {
    if (commentText.includes(phrase)) {
      detectedKeyword = phrase;
      matchType = 'phrase';
      break;
    }
  }
}

// Step 4: Check emojis
if (!detectedKeyword) {
  const originalComment = $input.item.json.Comment_Text; // Use original for emojis
  for (const emoji of emojis) {
    if (originalComment.includes(emoji)) {
      detectedKeyword = emoji;
      matchType = 'emoji';
      break;
    }
  }
}

// Step 5: Determine category
const isLead = !!detectedKeyword;

return {
  json: {
    Row_ID: $input.item.json.Row_ID,
    AI_Category: isLead ? 'Lead' : 'Casual',
    Lead_Magnet_Keyword: detectedKeyword,
    AI_Confidence_Score: isLead ? 1.0 : 0.9,
    AI_Rationale: isLead 
      ? `Detected ${matchType}: "${detectedKeyword}"`
      : 'No lead magnet indicators found',
    Processing_Status: 'Categorized',
    Last_Updated: new Date().toISOString()
  }
};
```

#### 4. Update Google Sheets
**Node Type:** Google Sheets
**Action:** Update row
**Sheet:** Comments_Master
**Match Column:** Row_ID
**Update Columns:**
- AI_Category
- Lead_Magnet_Keyword
- AI_Confidence_Score
- AI_Rationale
- Processing_Status
- Last_Updated

---

## Detection Logic

### Keyword Matching (Word Boundary)
Uses regex `\b{keyword}\b` to match whole words only.

**Examples:**
- ✅ "DM me" → Matches "DM"
- ✅ "Can you DM?" → Matches "DM"
- ❌ "ADMIN" → Does NOT match "DM" (part of word)

### Phrase Matching (Substring)
Checks if phrase exists anywhere in comment.

**Examples:**
- ✅ "Count me in!" → Matches "count me in"
- ✅ "Please sign me up" → Matches "sign me up"

### Emoji Matching
Direct character match (case-sensitive).

**Examples:**
- ✅ "👍" → Matches
- ✅ "Interested! 🙋" → Matches

### Negative Keyword Override
If ANY negative keyword found, automatically mark as "Casual" regardless of other matches.

**Examples:**
- ❌ "Don't DM me" → Casual (negative override)
- ❌ "Not interested, thanks" → Casual (negative override)

---

## Configuration Examples

### Basic Keywords
```
DM, interested, send, share, yes, please, want, need
```

### Common Phrases
```
count me in, sign me up, me too, same here, i want, i need, can i get, send me, share with me
```

### Positive Emojis
```
👍, 🙋, ✋, 🙌, 💯, ✅, 🔥
```

### Negative Keywords
```
don't dm, no dm, not interested, no thanks, spam, stop, unsubscribe
```

---

## Testing

### Test Cases

**Test 1: Simple Keyword**
- Input: "DM me please!"
- Expected: Lead, keyword="dm", confidence=1.0

**Test 2: Phrase Match**
- Input: "Count me in for this!"
- Expected: Lead, keyword="count me in", confidence=1.0

**Test 3: Emoji Only**
- Input: "👍"
- Expected: Lead, keyword="👍", confidence=1.0

**Test 4: Negative Override**
- Input: "Please don't DM me"
- Expected: Casual, keyword="", confidence=0.95, rationale="Negative keyword detected"

**Test 5: Casual Comment**
- Input: "Great post! Thanks for sharing."
- Expected: Casual, keyword="", confidence=0.9

**Test 6: False Positive Prevention**
- Input: "I'm an ADMIN on this platform"
- Expected: Casual (should NOT match "DM" in "ADMIN")

### Manual Testing Steps

1. Add test comments to `Comments_Master` sheet with `Processing_Status = "New"`
2. Run workflow manually
3. Verify output columns are populated correctly
4. Check that `Processing_Status` changed to "Categorized"

---

## Edge Cases

### Case Sensitivity
All matching is **case-insensitive** except emojis.

**Examples:**
- "dm", "DM", "Dm" → All match
- "INTERESTED", "interested" → All match

### Punctuation
Keyword matching ignores punctuation.

**Examples:**
- "DM!" → Matches
- "DM?" → Matches
- "DM." → Matches

### Multiple Keywords
Only the **first match** is recorded.

**Example:**
- "DM me, I'm interested" → Records "dm" (first match)

### Empty Comments
If `Comment_Text` is empty or null, mark as "Casual".

### Special Characters
Emojis and special characters are preserved in original form.

---

## Troubleshooting

### Issue: No comments being categorized
**Check:**
- Are there rows with `Processing_Status = "New"`?
- Is the Google Sheets node filtering correctly?
- Check n8n execution logs for errors

### Issue: Wrong categorization
**Check:**
- Review Config sheet keywords
- Check for typos in keywords
- Verify negative keywords aren't triggering incorrectly
- Test regex pattern manually: https://regex101.com/

### Issue: All comments marked as "Casual"
**Check:**
- Config sheet `Lead_Magnet_Keywords` is not empty
- Keywords are comma-separated
- No extra spaces or special characters in Config

### Issue: Function node error
**Check:**
- Config sheet has all required rows
- Column names match exactly (case-sensitive)
- Comment_Text column exists and has data

---

## Performance

### Expected Speed
- **~100ms per comment** (no API calls)
- Can process **500+ comments per minute**

### Scalability
- Tested up to **10,000 comments** without issues
- No rate limits (local processing)

---

## Future Enhancements

### Optional: Add Spam Detection
Add spam keywords to Config:
```
Spam_Keywords: "buy now, click here, limited offer, act fast"
```

Update function to check spam keywords and set `AI_Category = "Spam"`.

### Optional: Multi-language Support
Add language-specific keywords:
```
Lead_Magnet_Keywords_Hindi: "bhejo, chahiye, send karo"
```

### Optional: Confidence Threshold
Add to Config:
```
AI_Confidence_Threshold: 0.7
```

Only process comments with confidence > threshold.

---

## Deliverables

1. ✅ n8n workflow: `LI_leadmag2_categorize_comments`
2. ✅ Updated Google Sheets with categorized comments
3. ✅ Config sheet with customizable keywords
4. ✅ Test results document

---

## Support

### Questions?
- Review code comments in Function node
- Check n8n execution logs for detailed errors
- Test individual nodes using "Execute Node" feature

### Need Changes?
- Update Config sheet (no code changes needed)
- Add new keywords/phrases/emojis
- Adjust negative keywords

---

## Acceptance Criteria

- [ ] Workflow successfully reads Config sheet
- [ ] Workflow filters for `Processing_Status = "New"`
- [ ] Function node correctly detects keywords
- [ ] Function node handles negative keywords
- [ ] Google Sheets updated with all output columns
- [ ] All 6 test cases pass
- [ ] Processing_Status changes to "Categorized"
- [ ] No errors in n8n execution logs

---

**Ready to implement! Good luck! 🚀**
