async function runAIAnalysis() {
    const resultDiv = document.getElementById('aiResult');
    const aiButton = document.getElementById('AI-button');
    
    // 1. Show the loading state and disable the button
    aiButton.disabled = true;
    resultDiv.innerHTML = `
        <div class="ai-loading">
            <span class="spinner"></span> 
            Analyzing market trends... Please wait.
        </div>
    `;

    try {
        // Replace this with your actual input element ID to get the ticker dynamically
        const tickerValue = document.getElementById('ticker-input')?.value || "AAPL"; 
        
        // 2. Make your working fetch request
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: tickerValue, timeframe: "2-5 days" })
        });
        
        const data = await response.json();
        
        // 3. Render the successful results (adjust based on your actual response object structure)
        resultDiv.innerHTML = `<div class="ai-success">${data.detail || JSON.stringify(data)}</div>`;
        
    } catch (error) {
        // 4. Handle connection or server errors cleanly
        resultDiv.innerHTML = `<div class="ai-error">Error fetching analysis. Please try again.</div>`;
        console.error(error);
    } finally {
        // 5. Always re-enable the button when finished
        aiButton.disabled = false;
    }
}
