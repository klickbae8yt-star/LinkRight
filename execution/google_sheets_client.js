const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const TOKEN_PATH = path.join(__dirname, '../token.json');
const CREDENTIALS_PATH = path.join(__dirname, '../credentials.json');

// Load credentials and token
function getAuthClient() {
    if (!fs.existsSync(CREDENTIALS_PATH) || !fs.existsSync(TOKEN_PATH)) {
        throw new Error('Credentials or Token not found. Run authenticate_google.js first.');
    }

    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf-8'));
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf-8'));
    const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;

    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
    oAuth2Client.setCredentials(token);
    return oAuth2Client;
}

// Update a single row in Google Sheets
async function updateRow(sheetId, rowId, updates) {
    const auth = getAuthClient();
    const sheets = google.sheets({ version: 'v4', auth });

    // Map field names to column letters (assuming standard structure)
    // A: Row_ID, B: Timestamp, ... 
    // M: Connection_Status, N: Comment_Reply_Sent, O: Reply_Text, P: Reply_Timestamp
    // R: DM_Sent, S: DM_Timestamp, T: Lead_Magnet_Delivered, U: Error_Log, V: Last_Updated

    // Note: This mapping is fragile if columns change. 
    // Better approach: We update specific cells based on Row_ID (which corresponds to Row Number in Sheet)

    const range = `Comments_Master!M${rowId}:V${rowId}`; // Updating columns M to V

    // Construct the values array matching the columns M to V
    // M: Connection_Status
    // N: Comment_Reply_Sent
    // O: Comment_Reply_Text
    // P: Comment_Reply_Timestamp
    // Q: DM_Sent
    // R: DM_Sent_Timestamp
    // S: Lead_Magnet_Delivered
    // T: Error_Log
    // U: Last_Updated
    // V: Notes

    const values = [[
        updates.Connection_Status || '',
        updates.Comment_Reply_Sent || 'No',
        updates.Comment_Reply_Text || '',
        updates.Comment_Reply_Timestamp || '',
        updates.DM_Sent || 'No',
        updates.DM_Sent_Timestamp || '',
        updates.Lead_Magnet_Delivered || '',
        updates.Error_Log || '',
        new Date().toISOString(), // Last_Updated
        updates.Notes || ''
    ]];

    try {
        await sheets.spreadsheets.values.update({
            spreadsheetId: sheetId,
            range: range,
            valueInputOption: 'USER_ENTERED',
            resource: { values }
        });
        console.log(`✅ Updated Sheet Row ${rowId}`);
        return true;
    } catch (error) {
        console.error(`❌ Error updating sheet row ${rowId}:`, error.message);
        return false;
    }
}

module.exports = { updateRow };
