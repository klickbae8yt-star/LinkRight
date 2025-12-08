/**
 * Google Sheets OAuth Authentication Helper
 * Run this once to generate token.json
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];
const TOKEN_PATH = path.join(__dirname, '../token.json');
const CREDENTIALS_PATH = path.join(__dirname, '../credentials.json');

async function authorize() {
    // Load credentials
    if (!fs.existsSync(CREDENTIALS_PATH)) {
        console.error('❌ credentials.json not found!');
        console.log('\n📋 Steps to get credentials.json:');
        console.log('1. Go to https://console.cloud.google.com/');
        console.log('2. Create a new project or select existing');
        console.log('3. Enable Google Sheets API');
        console.log('4. Create OAuth 2.0 Client ID (Desktop app)');
        console.log('5. Download credentials.json');
        console.log('6. Place in project root\n');
        process.exit(1);
    }

    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf-8'));
    const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;

    const oAuth2Client = new google.auth.OAuth2(
        client_id,
        client_secret,
        redirect_uris[0]
    );

    // Check if we already have a token
    if (fs.existsSync(TOKEN_PATH)) {
        console.log('✅ token.json already exists!');
        const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf-8'));
        oAuth2Client.setCredentials(token);

        // Test the token
        const sheets = google.sheets({ version: 'v4', auth: oAuth2Client });
        try {
            await sheets.spreadsheets.get({ spreadsheetId: 'test' });
        } catch (error) {
            if (error.code === 404) {
                console.log('✅ Authentication successful! (Test sheet not found is expected)');
                return;
            }
        }
        console.log('✅ Authentication successful!');
        return;
    }

    // Get new token
    const authUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
    });

    console.log('\n🔐 Authorize this app by visiting this URL:');
    console.log('\n' + authUrl + '\n');

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    rl.question('Paste the full URL from the browser address bar here (even if it says error): ', (input) => {
        rl.close();

        // Extract code from URL if full URL is pasted
        let code = input.trim();
        if (code.includes('code=')) {
            const urlParams = new URLSearchParams(code.split('?')[1]);
            code = urlParams.get('code');
        }
        // Handle case where user pastes just the code or URL without ? (rare but possible)
        if (decodeURIComponent(code).includes('code=')) {
            // In case they pasted a fragment or something else
            const match = decodeURIComponent(code).match(/code=([^&]*)/);
            if (match) code = match[1];
        }

        oAuth2Client.getToken(code, (err, token) => {
            if (err) {
                console.error('❌ Error retrieving access token:', err);
                return;
            }

            oAuth2Client.setCredentials(token);

            // Save token
            fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2));
            console.log('\n✅ Token saved to token.json');
            console.log('✅ Authentication complete!');
            console.log('\nYou can now run: npm start');
        });
    });
}

authorize().catch(console.error);
