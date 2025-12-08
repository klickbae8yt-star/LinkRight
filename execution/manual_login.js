const { chromium } = require('playwright');
const fs = require('fs');
const readline = require('readline');

const CONFIG = {
    SESSION_FILE: './execution/linkedin_session.json',
    HEADLESS: false
};

async function manualLogin() {
    console.log('\n🔐 LinkedIn Manual Login Tool');
    console.log('=============================');

    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    try {
        console.log('🌐 Navigating to LinkedIn Login...');
        await page.goto('https://www.linkedin.com/login');

        console.log('\n👉 ACTION REQUIRED:');
        console.log('1. Browser window has opened.');
        console.log('2. Please log in manually with your email & password.');
        console.log('3. Complete 2FA if asked.');
        console.log('4. Ensure you reach the LinkedIn Feed (Home Page).');
        console.log('\n⌨️  When done, come back here and PRESS ENTER to save session...');

        // Wait for user input
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        await new Promise(resolve => {
            rl.question('', () => {
                rl.close();
                resolve();
            });
        });

        console.log('💾 Saving session...');
        const sessionData = await context.storageState();
        fs.writeFileSync(CONFIG.SESSION_FILE, JSON.stringify(sessionData, null, 2));
        console.log(`✅ Session saved to: ${CONFIG.SESSION_FILE}`);
        console.log('🚀 You can now run "npm start" for automation!');

    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await browser.close();
        process.exit(0);
    }
}

manualLogin();
