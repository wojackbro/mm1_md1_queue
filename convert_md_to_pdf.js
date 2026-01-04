const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { marked } = require('marked');

// Configure marked
marked.setOptions({
    breaks: true,
    gfm: true,
});

// Read markdown file
let mdContent = fs.readFileSync('PROJECT_REPORT.md', 'utf-8');

// Step 1: Protect LaTeX math by temporarily replacing it with placeholders
const mathPlaceholders = [];
let placeholderIndex = 0;

// Replace display math \[...\] with placeholders
mdContent = mdContent.replace(/\\\[([\s\S]*?)\\\]/g, (match, content) => {
    const placeholder = `__MATH_DISPLAY_${placeholderIndex}__`;
    mathPlaceholders[placeholderIndex] = { type: 'display', content: content.trim() };
    placeholderIndex++;
    return placeholder;
});

// Replace inline math \(...\) with placeholders  
mdContent = mdContent.replace(/\\\(([\s\S]*?)\\\)/g, (match, content) => {
    const placeholder = `__MATH_INLINE_${placeholderIndex}__`;
    mathPlaceholders[placeholderIndex] = { type: 'inline', content: content.trim() };
    placeholderIndex++;
    return placeholder;
});

// Step 2: Convert markdown to HTML
let htmlBody = marked(mdContent);

// Step 3: Restore LaTeX math with proper MathJax delimiters
mathPlaceholders.forEach((math, index) => {
    const placeholder = math.type === 'display' 
        ? `__MATH_DISPLAY_${index}__` 
        : `__MATH_INLINE_${index}__`;
    
    // Use \[...\] for display math and \(...\) for inline math
    const mathDelimiter = math.type === 'display' 
        ? `\\[${math.content}\\]` 
        : `\\(${math.content}\\)`;
    
    htmlBody = htmlBody.replace(placeholder, mathDelimiter);
});

// Step 4: Convert image paths to data URIs (base64)
const imageFiles = ['md1_lambda_0.5_mu_1.0.png', 'md1_lambda_0.9_mu_1.0.png'];
const imageDataURIs = {};

imageFiles.forEach(imageFile => {
    if (fs.existsSync(imageFile)) {
        const imageBuffer = fs.readFileSync(imageFile);
        const imageBase64 = imageBuffer.toString('base64');
        const imageExt = path.extname(imageFile).slice(1); // Remove the dot
        imageDataURIs[imageFile] = `data:image/${imageExt};base64,${imageBase64}`;
    }
});

// Replace image src attributes with data URIs
Object.keys(imageDataURIs).forEach(imageFile => {
    // Match <img src="filename.png" ...> or markdown image syntax ![alt](filename.png)
    const regex = new RegExp(`(src=["']|\\]\\(|href=["'])${imageFile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'g');
    htmlBody = htmlBody.replace(regex, (match, prefix) => {
        return prefix + imageDataURIs[imageFile];
    });
    
    // Also handle markdown image syntax that was converted to <img> tags
    htmlBody = htmlBody.replace(
        new RegExp(`(<img[^>]*src=["'])${imageFile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'g'),
        (match, prefix) => prefix + imageDataURIs[imageFile]
    );
});

// Create full HTML document with MathJax
const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page { margin: 2cm; }
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 100%;
            padding: 20px;
        }
        h1, h2, h3, h4 { page-break-after: avoid; }
        img { max-width: 100%; height: auto; page-break-inside: avoid; margin: 10px 0; display: block; }
        pre { page-break-inside: avoid; overflow-x: auto; background-color: #f4f4f4; padding: 10px; }
        code { font-family: 'Courier New', monospace; background-color: #f4f4f4; padding: 2px 4px; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        blockquote { border-left: 4px solid #ddd; margin-left: 0; padding-left: 20px; }
        p { margin: 0.5em 0; }
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
            }
        };
    </script>
</head>
<body>
${htmlBody}
</body>
</html>`;

async function convertToPdf() {
    console.log('Starting PDF conversion...');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    // Write HTML to temp file for debugging
    fs.writeFileSync('temp.html', htmlContent);
    console.log('HTML written to temp.html for debugging');
    
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    
    // Wait for MathJax to load and process
    await page.waitForFunction(() => {
        return typeof window.MathJax !== 'undefined' && window.MathJax.typesetPromise;
    }, { timeout: 10000 }).catch(() => {
        console.log('MathJax loading...');
    });
    
    // Typeset math
    await page.evaluate(() => {
        if (window.MathJax && window.MathJax.typesetPromise) {
            return window.MathJax.typesetPromise();
        }
    }).catch(err => console.log('MathJax typeset:', err));
    
    // Wait a bit more for rendering
    await page.waitForTimeout(4000);
    
    await page.pdf({
        path: 'PROJECT_REPORT.pdf',
        format: 'A4',
        margin: {
            top: '2cm',
            bottom: '2cm',
            left: '2cm',
            right: '2cm'
        },
        printBackground: true
    });
    
    await browser.close();
    console.log('PDF created successfully: PROJECT_REPORT.pdf');
}

convertToPdf().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
