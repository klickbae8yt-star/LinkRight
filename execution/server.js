const express = require('express');
const bodyParser = require('body-parser');
const { processSingleComment } = require('./linkedin_reply_automation');

const app = express();
const PORT = 3001;

app.use(bodyParser.json());

// Endpoint to trigger reply automation
app.post('/process-single-comment', async (req, res) => {
    console.log('📥 Received reply request:', req.body);

    // Extract parameters (support both camelCase and Google Sheets snake_case)
    const commentUrl = req.body.commentUrl || req.body.Comment_URL;
    const connectionDegree = req.body.connectionDegree || req.body.Connection_Degree;
    const keyword = req.body.keyword || req.body.Lead_Magnet_Keyword; // Assuming 'Lead_Magnet_Keyword' from scraper
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
        // Trigger automation (non-blocking if we want, but here we wait for result)
        const result = await processSingleComment(commentData);

        res.json({
            status: 'success',
            data: result
        });

    } catch (error) {
        console.error('❌ Error processing request:', error);
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log('👉 Send POST requests to /process-single-comment');
});
