const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { processSingleComment } = require('./linkedin_reply_automation');

const app = express();
const PORT = 3000;

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
        commentText: commentText || ''
    };

    try {
        const result = await processSingleComment(commentData);
        res.json({ status: 'success', data: result });
    } catch (error) {
        console.error('❌ Error processing request:', error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// Endpoint for Extension's Reply Automation button
app.post('/api/reply-automation/start', async (req, res) => {
    console.log('📥 Extension triggered reply automation:', req.body);

    // This endpoint is called by the extension
    // In future, it will read from Google Sheets and process comments
    res.json({
        status: 'success',
        message: 'Reply automation triggered. Processing will be handled by n8n workflow.',
        sheetsId: req.body.sheetsId
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log('👉 Endpoints available:');
    console.log('   POST /process-single-comment (n8n)');
    console.log('   POST /api/reply-automation/start (Extension)');
});
