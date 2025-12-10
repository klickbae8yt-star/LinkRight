const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios'); // Added axios for webhook calls
const { processSingleComment } = require('./linkedin_reply_automation');

const app = express();
const PORT = 3000;
const WEBHOOK_URL = 'https://n8n.linkright.in/webhook-test/smart-reply'; // Updated to Test URL

// CORS middleware - Allow requests from LinkedIn
app.use(cors({
    origin: ['https://www.linkedin.com', 'https://linkedin.com'],
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type']
}));

app.use(bodyParser.json());

// Endpoint to trigger reply automation (called by n8n)
app.post('/process-single-comment', async (req, res) => {
    console.log('📥 Received reply request:', req.body);

    // Extract parameters (support both camelCase and Google Sheets snake_case)
    const commentUrl = req.body.commentUrl || req.body.Comment_URL;
    const connectionDegree = req.body.connectionDegree || req.body.Connection_Degree;
    const keyword = req.body.keyword || req.body.Lead_Magnet_Keyword;
    const rowId = req.body.rowId || req.body.Row_ID;
    const commenterName = req.body.commenterName || req.body.Commenter_Name;
    const commenterProfileUrl = req.body.commenterProfileUrl || req.body.Commenter_Profile_URL;
    const commentText = req.body.commentText || req.body.Comment_Text;
    const commentUrnId = req.body.commentUrnId || req.body.Comment_URN_ID; // Ensure we get the ID

    if (!commentUrl) {
        return res.status(400).json({ error: 'Missing commentUrl (or Comment_URL)' });
    }

    // Construct comment object expected by automation script
    const commentData = {
        commentUrl,
        connectionDegree,
        keyword,
        Row_ID: rowId,
        commenterName: commenterName || 'Unknown',
        commenterProfileUrl: commenterProfileUrl || '',
        commentText: commentText || '',
        commentUrnId
    };

    try {
        // 1. Run Automation Script (Scrape & Decide)
        const result = await processSingleComment(commentData);

        // 2. Handle AI Reply Case
        if (result.status === 'ai_reply_needed') {
            console.log('🤖 AI Reply Needed. Calling Webhook with Rich Payload...');

            try {
                // Call AI Webhook
                const webhookResponse = await axios.post(WEBHOOK_URL, result.payload);
                // Handle various response formats from n8n
                const aiReplyText = webhookResponse.data.reply || webhookResponse.data.text || webhookResponse.data.output || "Thanks for sharing!";

                console.log(`✨ AI Reply Generated: "${aiReplyText}"`);

                // 3. Post the AI Reply (Re-using Playwright logic with Force Mode)
                console.log('🚀 Re-launching browser to post AI reply...');
                const postResult = await processSingleComment({
                    ...commentData,
                    forceReplyMessage: aiReplyText // Force the script to just post this message
                });

                res.json({ status: 'success', data: postResult });

            } catch (webhookError) {
                console.error('❌ Webhook Error:', webhookError.message);
                res.status(500).json({ status: 'error', message: 'AI Webhook failed' });
            }

        } else {
            // Standard success (e.g. Reply to Connect)
            res.json({ status: 'success', data: result });
        }

    } catch (error) {
        console.error('❌ Error processing request:', error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});

app.post('/api/reply-automation/start', async (req, res) => {
    console.log('📥 Extension triggered reply automation:', req.body);
    res.json({
        status: 'success',
        message: 'Reply automation triggered. Processing will be handled by n8n workflow.',
        sheetsId: req.body.sheetsId
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
