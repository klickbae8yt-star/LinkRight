// ============================================
// LinkedIn Comment Scraper - Console Snippet
// ============================================
// Copy-paste this in LinkedIn post page console (F12 → Console tab)
// After manually scrolling to load all comments

(function () {
    console.log('🚀 Starting LinkedIn comment extraction...');

    const comments = [];
    const seen = new Set();

    // Get current post URL and title
    const postUrl = window.location.href;
    const postTitle = document.querySelector('.feed-shared-update-v2__description')?.textContent.trim().substring(0, 100) || 'LinkedIn Post';

    // Find all comment articles
    const commentElements = document.querySelectorAll('article.comments-comment-entity');
    console.log(`📊 Found ${commentElements.length} comment elements`);

    commentElements.forEach(article => {
        try {
            // Get unique comment ID
            const commentId = article.getAttribute('data-id');

            // Skip duplicates
            if (!commentId || seen.has(commentId)) return;
            seen.add(commentId);

            // Determine Type (Parent vs Reply)
            const isReply = article.classList.contains('comments-comment-entity--reply');
            const commentType = isReply ? 'Reply' : 'Parent';

            // Extract Parent ID (if it's a reply)
            let parentId = '';
            if (isReply) {
                // The parent ID is usually in the same thread container or we can infer it
                // For now, let's look for the closest parent thread item
                // NOTE: LinkedIn DOM is complex. A simple way is to find the preceding 'parent' comment in our list
                // But a more robust way for the scraper is to look at the DOM hierarchy if possible.
                // Actually, for 'Reply', the parent is the main comment of the thread.
                // Let's try to find the closest previous article that is NOT a reply? No, that might be wrong.
                // Better approach: The data-id often contains the parent info or we can leave it blank for now 
                // and let n8n handle it by "Thread URL" or just treat them as separate for now.
                // User requirement: "add one more column which says if it is like a parent comment or ... nested"
                // So just identifying Type is enough for now.
            }

            // Extract all fields matching Comments_Master.csv structure
            const nameEl = article.querySelector('.comments-comment-meta__description-title');
            const commenterName = nameEl ? nameEl.textContent.trim() : '';

            const profileEl = article.querySelector('a.comments-comment-meta__description-container');
            let commenterProfileUrl = profileEl ? profileEl.getAttribute('href') : '';
            if (commenterProfileUrl && !commenterProfileUrl.startsWith('http')) {
                commenterProfileUrl = 'https://www.linkedin.com' + commenterProfileUrl;
            }

            const headlineEl = article.querySelector('.comments-comment-meta__description-subtitle');
            const commenterHeadline = headlineEl ? headlineEl.textContent.trim() : '';

            const textEl = article.querySelector('.comments-comment-item__main-content');
            const commentText = textEl ? textEl.textContent.trim() : '';

            const timeEl = article.querySelector('time.comments-comment-meta__data');
            const timestamp = timeEl ? timeEl.textContent.trim() : '';

            // Build proper LinkedIn comment URL
            let commentUrl = '';
            if (commentId) {
                // Extract activity/ugcPost ID and comment ID from URN
                // Format: urn:li:comment:(activity:7402394519830216704,7402396422115172352)
                // OR: urn:li:comment:(ugcPost:7388366643141181440,7388368822958718977)
                const typeMatch = commentId.match(/(activity|ugcPost):(\d+)/);
                const commentMatch = commentId.match(/,(\d+)\)/);

                if (typeMatch && commentMatch) {
                    const postType = typeMatch[1]; // 'activity' or 'ugcPost'
                    const postId = typeMatch[2];
                    const commentOnlyId = commentMatch[1];

                    // Build URL with proper encoding and BOTH required parameters
                    // commentUrn: identifies the comment (activity first, comment second)
                    const encodedCommentUrn = `urn%3Ali%3Acomment%3A%28${postType}%3A${postId}%2C${commentOnlyId}%29`;

                    // dashCommentUrn: triggers auto-scroll (comment first, activity second - reversed!)
                    const encodedDashCommentUrn = `urn%3Ali%3Afsd_comment%3A%28${commentOnlyId}%2Curn%3Ali%3A${postType}%3A${postId}%29`;

                    // Complete URL with dynamic post type in base URL
                    commentUrl = `https://www.linkedin.com/feed/update/urn:li:${postType}:${postId}?commentUrn=${encodedCommentUrn}&dashCommentUrn=${encodedDashCommentUrn}`;
                }
            }

            // Current timestamp for Timestamp_Captured
            const now = new Date();
            const timestampCaptured = now.toISOString().replace('T', ' ').substring(0, 19);

            // Only add if has essential data
            if (commenterName && commentText) {
                comments.push({
                    // Row_ID removed to let Google Sheets formula handle it
                    Timestamp_Captured: timestampCaptured,
                    Post_URL: postUrl,
                    Post_Title: postTitle,
                    Commenter_Name: commenterName,
                    Commenter_Profile_URL: commenterProfileUrl,
                    Commenter_Headline: commenterHeadline,
                    Comment_Text: commentText,
                    Comment_Text: commentText,
                    Comment_URL: commentUrl,
                    Comment_ID: commentId, // Unique ID for verification
                    Comment_Type: commentType, // Parent or Reply

                    // Categorization (n8n)
                    Lead_Magnet_Keyword: '',
                    AI_Category: '',
                    Processing_Status: 'New',

                    // Connection Check (Scraper Extraction)
                    // Logic: Look for "• 1st", "• 2nd", "• 3rd" in the comment metadata
                    Connection_Degree: (function () {
                        // Use the specific selector from user's snippet
                        const metaData = article.querySelector('.comments-comment-meta__data');
                        const text = metaData ? metaData.textContent : article.textContent;

                        // Check for the specific bullet character • followed by degree
                        if (text.includes('• 1st')) return '1st';
                        if (text.includes('• 2nd')) return '2nd';
                        if (text.includes('• 3rd')) return '3rd';

                        // Fallback: Check for "1st", "2nd", "3rd" with other separators if needed
                        // But user specifically asked for "• 2nd" pattern

                        return 'None';
                    })(),

                    // Actions
                    Comment_Reply_Sent: 'No',
                    Comment_Reply_Text: '',
                    Comment_Reply_Timestamp: '',
                    DM_Sent: 'No',
                    DM_Sent_Timestamp: '',

                    // Outcome
                    Lead_Magnet_Delivered: '',

                    // Logs
                    Error_Log: '',
                    Last_Updated: timestampCaptured,
                    Notes: ''
                });
            }

        } catch (error) {
            console.error('❌ Error parsing comment:', error);
        }
    });

    console.log(`✅ Successfully extracted ${comments.length} comments`);

    // Display preview in console
    console.table(comments.slice(0, 5)); // Show first 5

    // Convert to CSV format
    const headers = Object.keys(comments[0] || {});
    const csvRows = [headers.join(',')];

    comments.forEach(comment => {
        const values = headers.map(header => {
            const value = comment[header] || '';
            // Escape commas and quotes in CSV
            const escaped = String(value).replace(/"/g, '""');
            return `"${escaped}"`;
        });
        csvRows.push(values.join(','));
    });

    const csvContent = csvRows.join('\n');

    // Copy to clipboard
    const textarea = document.createElement('textarea');
    textarea.value = csvContent;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);

    console.log('📋 CSV data copied to clipboard!');
    console.log('📊 Total comments:', comments.length);
    console.log('');
    console.log('✨ Next steps:');
    console.log('1. Open Google Sheets');
    console.log('2. Go to Comments_Master sheet');
    console.log('3. Paste (Cmd+V / Ctrl+V)');
    console.log('4. Data will import automatically!');

    alert(`✅ ${comments.length} comments copied to clipboard as CSV!\n\nPaste directly into Google Sheets.`);

    return comments;
})();
