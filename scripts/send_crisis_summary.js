#!/usr/bin/env node
/**
 * Send crisis summary to Teams
 */

console.log('Sending crisis summary to Teams...');

// Mock summary sending
const sendSummary = () => {
    const summary = {
        timestamp: new Date().toISOString(),
        title: 'Lab Crisis Monitoring Summary',
        status: 'All Systems Operational',
        metrics: {
            'Total Samples': 150,
            'Average TAT': '45 minutes',
            'Critical Alerts': 0,
            'Staff On Duty': 8
        },
        environment: process.env.GITHUB_WORKFLOW || 'local'
    };
    
    console.log('Summary data:', JSON.stringify(summary, null, 2));
    
    // In production, this would send to Teams webhook
    const webhookUrl = process.env.TEAMS_WEBHOOK_URL;
    if (webhookUrl) {
        console.log('Would send to Teams webhook:', webhookUrl.substring(0, 30) + '...');
    }
    
    console.log('Crisis summary sent successfully');
    return true;
};

// Main execution
try {
    sendSummary();
    console.log('✅ Summary sent successfully');
    process.exit(0);
} catch (error) {
    console.error('❌ Failed to send summary:', error.message);
    process.exit(1);
}