/**
 * Ticker Search Functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Setup ticker input with autocomplete
    setupTickerInput();
});

function setupTickerInput() {
    const tickerInput = document.getElementById('ticker-input');
    const suggestionsDiv = document.getElementById('ticker-suggestions');
    
    if (!tickerInput) return;
    
    // Input event for search suggestions
    tickerInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        
        if (query.length < 1) {
            suggestionsDiv.classList.remove('active');
            return;
        }
        
        // Search for matching tickers
        fetch(`/api/search-tickers?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data.results, tickerInput);
            })
            .catch(error => {
                console.error('Error searching tickers:', error);
            });
    });
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target !== tickerInput && !suggestionsDiv.contains(e.target)) {
            suggestionsDiv.classList.remove('active');
        }
    });
}

function displaySuggestions(results, inputElement) {
    const suggestionsDiv = document.getElementById('ticker-suggestions');
    
    if (!results || results.length === 0) {
        suggestionsDiv.classList.remove('active');
        return;
    }
    
    suggestionsDiv.innerHTML = '';
    
    results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.innerHTML = `
            <strong>${result.symbol}</strong><br>
            <small>${result.name}</small>
        `;
        
        item.addEventListener('click', function() {
            inputElement.value = result.symbol;
            suggestionsDiv.classList.remove('active');
            
            // Trigger load if load button exists
            const loadBtn = document.getElementById('load-button');
            if (loadBtn) {
                loadBtn.click();
            }
        });
        
        suggestionsDiv.appendChild(item);
    });
    
    suggestionsDiv.classList.add('active');
}

/**
 * Validate and select ticker
 */
function validateAndSelectTicker(ticker) {
    ticker = ticker.trim().toUpperCase();
    
    if (!ticker) {
        console.error('No ticker provided');
        return false;
    }
    
    // Validate ticker via API
    fetch(`/api/validate-ticker/${ticker}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Invalid ticker');
            }
            return response.json();
        })
        .then(data => {
            // Store in session for pages to use
            sessionStorage.setItem('selected_ticker', ticker);
            console.log(`Ticker ${ticker} validated and selected`);
        })
        .catch(error => {
            console.error('Ticker validation failed:', error);
        });
    
    return true;
}

// Export functions globally
window.validateAndSelectTicker = validateAndSelectTicker;
