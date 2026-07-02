const fs = require('fs');
const path = require('path');

const SUBFOLDER = './reports'; // Your subfolder
const INDEX_FILE = './index.html';

// 1. Read files from the subfolder
fs.readdir(SUBFOLDER, (err, files) => {
    if (err) return console.error('Could not scan directory:', err);

    // 2. Filter for only HTML files
    const htmlFiles = files.filter(file => path.extname(file) === '.html');
    
    // 3. Generate HTML markup for both sections
    const linksHtml = htmlFiles
        .map(file => `            <li><a href="${SUBFOLDER}/${file}">${file}</a></li>`)
        .join('\n');
        
    // Generates values formatted as NASDAQ:SYMBOL (e.g., NASDAQ:AAPL)
    const dropdownHtml = htmlFiles
        .map(file => {
            const symbol = path.basename(file, '.html').toUpperCase();
            return `            <option value="NASDAQ:${symbol}">${symbol}</option>`;
        })
        .join('\n');

    // 4. Read the current index.html file
    let htmlContent = fs.readFileSync(INDEX_FILE, 'utf8');

    // 5. Define Regex targets for BOTH the list and the dropdown select menu
    const listRegex = /(<ul id="dynamic-links-container">)[\s\S]*?(<\/ul>)/;
    const dropdownRegex = /(<select id="ticker-select"[^>]*>[\s\S]*?<option value="">.*?<\/option>)[\s\S]*?(<\/select>)/;

    let updated = false;

    // Update the list container
    if (listRegex.test(htmlContent)) {
        htmlContent = htmlContent.replace(listRegex, `$1\n${linksHtml}\n        $2`);
        updated = true;
    } else {
        console.warn('Warning: Could not find id="dynamic-links-container" in index.html');
    }

    // Update the dropdown menu (keeping the very first default option)
    if (dropdownRegex.test(htmlContent)) {
        htmlContent = htmlContent.replace(dropdownRegex, `$1\n${dropdownHtml}\n    $2`);
        updated = true;
    } else {
        console.warn('Warning: Could not find id="ticker-select" with a default option in index.html');
    }

    // 6. Save the updated file if any changes were successfully targeted
    if (updated) {
        fs.writeFileSync(INDEX_FILE, htmlContent);
        console.log('Success: Top section links and dropdown menu options updated successfully!');
    } else {
        console.error('Error: No targets found. File was not written.');
    }
});
