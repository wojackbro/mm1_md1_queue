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

// Step 1: Convert images to base64 BEFORE markdown processing
const imageFiles = ['md1_lambda_0.5_mu_1.0.png', 'md1_lambda_0.9_mu_1.0.png'];
const imageDataURIs = {};

imageFiles.forEach(imageFile => {
    if (fs.existsSync(imageFile)) {
        const imageBuffer = fs.readFileSync(imageFile);
        const imageBase64 = imageBuffer.toString('base64');
        const imageExt = path.extname(imageFile).slice(1);
        imageDataURIs[imageFile] = `data:image/${imageExt};base64,${imageBase64}`;
        
        // Replace markdown image syntax with HTML img tag using data URI
        const imageRegex = new RegExp(`!\\[([^\\]]*)\\]\\(${imageFile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\)`, 'g');
        mdContent = mdContent.replace(imageRegex, (match, alt) => {
            return `<img src="${imageDataURIs[imageFile]}" alt="${alt}" style="max-width: 100%; height: auto; margin: 10px 0;" />`;
        });
    }
});

// Step 2: Protect LaTeX math by temporarily replacing it with placeholders
const mathPlaceholders = [];
let placeholderIndex = 0;

// Replace display math \[...\] with placeholders (use unique markers)
mdContent = mdContent.replace(/\\\[([\s\S]*?)\\\]/g, (match, content) => {
    const placeholder = `__MATH_DISPLAY_${placeholderIndex}__`;
    mathPlaceholders.push({ type: 'display', content: content.trim(), placeholder });
    placeholderIndex++;
    return `\n\n${placeholder}\n\n`;
});

// Replace inline math \(...\) with placeholders  
mdContent = mdContent.replace(/\\\(([\s\S]*?)\\\)/g, (match, content) => {
    const placeholder = `__MATH_INLINE_${placeholderIndex}__`;
    mathPlaceholders.push({ type: 'inline', content: content.trim(), placeholder });
    placeholderIndex++;
    return placeholder;
});

// Step 3: Convert markdown to HTML
let htmlBody = marked(mdContent);

// Step 4: Restore LaTeX math with proper MathJax delimiters
mathPlaceholders.forEach((math) => {
    // The content already has proper LaTeX syntax, just need to wrap it
    const mathDelimiter = math.type === 'display' 
        ? `\\[${math.content}\\]` 
        : `\\(${math.content}\\)`;
    
    // Replace placeholder - handle cases where marked might wrap it in <p> tags
    const patterns = [
        new RegExp(`<p>\\s*${math.placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*</p>`, 'g'),
        new RegExp(math.placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')
    ];
    
    patterns.forEach(pattern => {
        htmlBody = htmlBody.replace(pattern, mathDelimiter);
    });
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
    
    // Wait for MathJax to load
    await page.waitForFunction(() => {
        return typeof window.MathJax !== 'undefined';
    }, { timeout: 15000 });
    
    // Wait for MathJax to be ready and typeset
    await page.evaluate(() => {
        return new Promise((resolve) => {
            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise().then(() => {
                    setTimeout(resolve, 1000);
                });
            } else {
                setTimeout(resolve, 3000);
            }
        });
    });
    
    // Additional wait to ensure rendering is complete
    await page.waitForTimeout(2000);
    
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
    console.log('Check temp.html to verify HTML output');
}

convertToPdf().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
