# Google Sheets Templates - Import Instructions

## Overview
These CSV templates are ready to import into Google Sheets to set up your LinkedIn Lead Magnet automation system.

## Files Included

1. **Comments_Master.csv** - Main comment tracking sheet
2. **DMs_Master.csv** - Direct message management
3. **Leads_CRM.csv** - Qualified leads database
4. **Config.csv** - Configuration settings
5. **Analytics_Dashboard.csv** - Metrics and analytics

## Import Instructions

### Step 1: Create New Google Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Click **"Blank"** to create new spreadsheet
3. Name it: **"LinkedIn Lead Magnet Automation"**

### Step 2: Import Each CSV

For each CSV file:

1. **Create a new sheet tab** (click + at bottom)
2. **Rename the tab** to match the CSV name (e.g., "Comments_Master")
3. **Go to File → Import**
4. **Upload** the corresponding CSV file
5. **Import settings:**
   - Import location: **"Replace current sheet"**
   - Separator type: **"Comma"**
   - Convert text to numbers: **"No"** (keep as text)
   - Click **"Import data"**

Repeat for all 5 CSV files.

### Step 3: Set Up Data Validation

#### Comments_Master Sheet
- Column K (AI_Category): Dropdown → `Lead, Casual, Spam`
- Column N (Connection_Status): Dropdown → `Connected, Not Connected, Pending`
- Column O (Processing_Status): Dropdown → `New, Categorized, Processed, Delivered, Failed`
- Column P (Comment_Reply_Sent): Dropdown → `Yes, No`
- Column S (DM_Sent): Dropdown → `Yes, No`

#### DMs_Master Sheet
- Column F (Contains_Keyword): Dropdown → `Yes, No`
- Column H (AI_Category): Dropdown → `Lead, Question, Casual, Spam`
- Column J (Connection_Status): Dropdown → `Connected, Not Connected`
- Column K (Processing_Status): Dropdown → `New, Categorized, Replied, Ignored, Checked`
- Column L (Reply_Sent): Dropdown → `Yes, No`
- Column P (Duplicate_Check): Dropdown → `Yes, No`

#### Leads_CRM Sheet
- Column J (Lead_Source): Dropdown → `Comment, DM, Both`
- Column N (Status): Dropdown → `New, Contacted, Qualified, Customer, Lost`
- Column O (Cold_Email_Sent): Dropdown → `Yes, No`
- Column Q (Cold_Email_Response): Dropdown → `No Response, Interested, Not Interested`

### Step 4: Conditional Formatting

#### Comments_Master Sheet
1. Select column O (Processing_Status)
2. Format → Conditional formatting
3. Add rules:
   - **Failed** → Red background
   - **Delivered** → Green background
   - **Categorized** → Yellow background
   - **New** → Light blue background

#### DMs_Master Sheet
1. Select column K (Processing_Status)
2. Add same color rules as above

### Step 5: Protect Config Sheet
1. Click on **Config** tab
2. Right-click → **Protect sheet**
3. Set permissions: **"Only you can edit"**
4. Add warning: **"Warning when editing this range"**

### Step 6: Share with n8n
1. Click **Share** button (top right)
2. Add your **n8n service account email**
3. Set permission: **Editor**
4. Click **Send**

## Customization

### Update Config Sheet
Before starting automation, update these values in **Config** sheet:

- **Lead_Magnet_Resource_URL**: Your actual Google Drive/PDF link
- **Daily_Activator_Email**: Your email address
- **Post_URLs_To_Monitor**: Your LinkedIn post URLs
- **Lead_Magnet_Keywords**: Add/remove keywords as needed

### Customize Templates
Edit these message templates to match your brand voice:
- **Lead_Magnet_DM_Template**
- **Comment_Reply_Template**
- **Non_Connected_Message**

## Sample Data

Each CSV includes 2-3 sample rows to show the data structure. You can:
- **Keep them** as examples while testing
- **Delete them** before going live

## Analytics Dashboard Setup

The Analytics_Dashboard formulas reference other sheets. After import:

1. Verify all formulas are working
2. Check that sheet names match exactly
3. Formulas will auto-calculate as data populates

## Troubleshooting

### Formulas Not Working
- Ensure sheet names are exact: `Comments_Master`, `DMs_Master`, `Leads_CRM`
- Check that column references match your data

### Import Errors
- Make sure separator is set to **Comma**
- Disable "Convert text to numbers" to preserve formatting

### Dropdown Not Showing
- Manually add data validation (see Step 3)

## Next Steps

After importing:
1. ✅ Verify all 5 sheets are created
2. ✅ Set up data validation dropdowns
3. ✅ Add conditional formatting
4. ✅ Protect Config sheet
5. ✅ Update Config values
6. ✅ Share with n8n service account
7. ✅ Test by adding a sample row manually

## Support

For detailed column explanations, see: `google_sheets_structure.md`
