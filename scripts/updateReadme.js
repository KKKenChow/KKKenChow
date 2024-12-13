// scripts/updateReadme.js
const fs = require('fs');
const axios = require('axios');

async function fetchTodayInHistory() {
    const date = new Date();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const day = String(date.getDate()).padStart(2, '0');
    
    try {
        const response = await axios.get(`http://history.muffinlabs.com/date/${month}/${day}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching data from API:", error);
        return null;
    }
}

function updateReadme(data) {
    let readmeContent = fs.readFileSync('README.md', 'utf8');
    const historySection = `## 历史上的今天\n\n`;

    if (!readmeContent.includes(historySection)) {
        readmeContent += historySection;
    }

    // 更新或添加历史上的今天内容
    const events = data.data.Events.map(event => `- ${event.year}: ${event.text}`).join('\n');
    const updatedReadme = readmeContent.replace(/## 历史上的今天([\s\S]*?)\n/, `${historySection}${events}\n`);

    fs.writeFileSync('README.md', updatedReadme, 'utf8');
}

(async () => {
    const data = await fetchTodayInHistory();
    if (data) {
        updateReadme(data);
        console.log("README updated with today's historical events.");
    }
})();
