/**
 * Stock Dashboard - Main JavaScript
 */

// Update footer timestamp
function updateTimestamp() {
    const now = new Date();
    document.getElementById('update-time').textContent = now.toLocaleString();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateTimestamp();
    
    // Update timestamp every minute
    setInterval(updateTimestamp, 60000);
});

// Utility functions
const Utils = {
    /**
     * Format currency
     */
    formatCurrency: function(value) {
        if (!value && value !== 0) return 'N/A';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    },

    /**
     * Format large numbers with K, M, B suffix
     */
    formatNumber: function(num) {
        if (!num && num !== 0) return 'N/A';
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(2) + 'B';
        }
        if (num >= 1000000) {
            return (num / 1000000).toFixed(2) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(2) + 'K';
        }
        return num.toFixed(2);
    },

    /**
     * Format percentage
     */
    formatPercent: function(value) {
        if (!value && value !== 0) return 'N/A';
        const sign = value > 0 ? '+' : '';
        return sign + value.toFixed(2) + '%';
    },

    /**
     * Format date
     */
    formatDate: function(dateStr) {
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US');
        } catch (e) {
            return dateStr;
        }
    },

    /**
     * Fetch with error handling
     */
    apiFetch: async function(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    },

    /**
     * Create element with classes
     */
    createElement: function(tag, classes = '', text = '') {
        const element = document.createElement(tag);
        if (classes) {
            element.className = classes;
        }
        if (text) {
            element.textContent = text;
        }
        return element;
    }
};

// Chart utilities
const ChartUtils = {
    /**
     * Generate random color with alpha
     */
    getColor: function(type) {
        const colors = {
            primary: '#2563eb',
            success: '#16a34a',
            error: '#dc2626',
            warning: '#f59e0b',
            info: '#0891b2'
        };
        return colors[type] || colors.primary;
    }
};

// Export utilities
window.Utils = Utils;
window.ChartUtils = ChartUtils;
