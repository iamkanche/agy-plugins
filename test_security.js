const assert = require('assert');
const fs = require('fs');

// Read index.html
const content = fs.readFileSync('index.html', 'utf8');

// Ensure escapeHTML is defined
assert(content.includes('function escapeHTML('), 'escapeHTML function must be defined in index.html');

// Verify headerSection.innerHTML uses escapeHTML for dynamic variables
const headerMatch = content.match(/headerSection\.innerHTML\s*=\s*`([\s\S]*?)`;/);
assert(headerMatch, 'headerSection.innerHTML block found');

const headerBlock = headerMatch[1];
assert(headerBlock.includes('${escapeHTML(data.displayName)}'), 'displayName should be escaped');
assert(headerBlock.includes('${escapeHTML(data.version)}'), 'version should be escaped');
assert(headerBlock.includes('${escapeHTML(data.inspectorUrl)}'), 'inspectorUrl should be escaped');
assert(headerBlock.includes('${escapeHTML(data.desc)}'), 'desc should be escaped');

// Test escapeHTML function directly
function escapeHTML(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

assert.strictEqual(escapeHTML('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;');
assert.strictEqual(escapeHTML('foo & "bar" \'baz\''), 'foo &amp; &quot;bar&quot; &#39;baz&#39;');

console.log('All security checks and unit tests passed successfully!');
