const BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com"; // Replace with your PythonAnywhere URL

async function fetchData() {
    const response = await fetch(`${BASE_URL}/crypto-prices`);
    const prices = await response.json();
    
    const tableBody = document.getElementById("crypto-data");
    tableBody.innerHTML = ""; // Clear existing rows
    
    for (const coin in prices) {
        const sentimentRes = await fetch(`${BASE_URL}/sentiment/${coin}`);
        const sentimentData = await sentimentRes.json();
        const predictRes = await fetch(`${BASE_URL}/price-predict/${coin}`);
        const predictData = await predictRes.json();
        
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${coin}</td>
            <td>${prices[coin].toFixed(2)}</td>
            <td>${sentimentData.sentiment.toFixed(2)}</td>
            <td>${predictData.predicted_price.toFixed(2)}</td>
        `;
        tableBody.appendChild(row);
    }
}

function refreshData() {
    fetchData().catch(err => console.error("Error fetching data:", err));
}

// Load data on page load
window.onload = refreshData;