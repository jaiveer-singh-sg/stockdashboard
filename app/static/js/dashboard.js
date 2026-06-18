async function runAIAnalysis() {
    const resultDiv = document.getElementById('aiResult');
    const aiButton = document.getElementById('AI-button');
    const modal = document.getElementById('aiModal');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');
    
    aiButton.disabled = true;
    resultDiv.innerHTML = `<div class="ai-loading"><span class="spinner"></span> Running Agent Protocols...</div>`;

    try {
        const tickerValue = document.getElementById('ticker-input')?.value || "NVDA"; 
        
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: tickerValue, timeframe: "2-5 days" })
        });
        
        let data = await response.json();
        
        // Safety Clean: Strip leading random characters if your server returned a corrupt string "m{...}"
        if (typeof data === 'string' && data.startsWith('m{')) {
            data = JSON.parse(data.substring(1));
        }

        // Clear the layout loading state text completely
        resultDiv.innerHTML = "";

        // Build elegant structured HTML out of your JSON metrics
        modalTitle.innerText = `📈 ${tickerValue.toUpperCase()} - Swing Trade Insights`;
        modalBody.innerHTML = `
            <div class="metric-grid">
                <div class="metric-card"><strong>Trend:</strong> <span class="badge ${data.trend?.toLowerCase()}">${data.trend}</span></div>
                <div class="metric-card"><strong>Technical Score:</strong> ${data.technical_score}/100</div>
                <div class="metric-card"><strong>Entry Point:</strong> ${data.entry}</div>
                <div class="metric-card"><strong>Stop Loss:</strong> 🛑 ${data.stop_loss}</div>
                <div class="metric-card"><strong>Target Price:</strong> 🎯 ${data.target}</div>
                <div class="metric-card"><strong>Risk/Reward:</strong> ⚖️ ${data.risk_reward}</div>
            </div>

            <div class="case-split">
                <div class="case-box bull">
                    <h4>🟢 Bull Case</h4>
                    <ul>${data.bull_case?.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                </div>
                <div class="case-box bear">
                    <h4>🔴 Bear Case</h4>
                    <ul>${data.bear_case?.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                </div>
            </div>

            <div class="final-view-box">
                <h4>📋 Analyst Summary</h4>
                <p>${data.final_view}</p>
            </div>
        `;
        
        // Launch the native HTML popup box centered over your layout page
        modal.showModal();
        
    } catch (error) {
        resultDiv.innerHTML = `<div class="ai-error">Error fetching analysis. Please try again.</div>`;
        console.error(error);
    } finally {
        aiButton.disabled = false;
    }
}
async function runAIAnalysis() {
    const resultDiv = document.getElementById('aiResult');
    const aiButton = document.getElementById('AI-button');
    const modal = document.getElementById('aiModal');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');
    
    aiButton.disabled = true;
    resultDiv.innerHTML = `<div class="ai-loading"><span class="spinner"></span> Running Agent Protocols...</div>`;

    try {
        const tickerValue = document.getElementById('ticker-input')?.value || "NVDA"; 
        
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: tickerValue, timeframe: "2-5 days" })
        });
        
        let data = await response.json();
        
        // Safety Clean: Strip leading random characters if your server returned a corrupt string "m{...}"
        if (typeof data === 'string' && data.startsWith('m{')) {
            data = JSON.parse(data.substring(1));
        }

        // Clear the layout loading state text completely
        resultDiv.innerHTML = "";

        // Build elegant structured HTML out of your JSON metrics
        modalTitle.innerText = `📈 ${tickerValue.toUpperCase()} - Swing Trade Insights`;
        modalBody.innerHTML = `
            <div class="metric-grid">
                <div class="metric-card"><strong>Trend:</strong> <span class="badge ${data.trend?.toLowerCase()}">${data.trend}</span></div>
                <div class="metric-card"><strong>Technical Score:</strong> ${data.technical_score}/100</div>
                <div class="metric-card"><strong>Entry Point:</strong> ${data.entry}</div>
                <div class="metric-card"><strong>Stop Loss:</strong> 🛑 ${data.stop_loss}</div>
                <div class="metric-card"><strong>Target Price:</strong> 🎯 ${data.target}</div>
                <div class="metric-card"><strong>Risk/Reward:</strong> ⚖️ ${data.risk_reward}</div>
            </div>

            <div class="case-split">
                <div class="case-box bull">
                    <h4>🟢 Bull Case</h4>
                    <ul>${data.bull_case?.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                </div>
                <div class="case-box bear">
                    <h4>🔴 Bear Case</h4>
                    <ul>${data.bear_case?.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                </div>
            </div>

            <div class="final-view-box">
                <h4>📋 Analyst Summary</h4>
                <p>${data.final_view}</p>
            </div>
        `;
        
        // Launch the native HTML popup box centered over your layout page
        modal.showModal();
        
    } catch (error) {
        resultDiv.innerHTML = `<div class="ai-error">Error fetching analysis. Please try again.</div>`;
        console.error(error);
    } finally {
        aiButton.disabled = false;
    }
}
