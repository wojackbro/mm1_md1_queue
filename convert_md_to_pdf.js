const fs = require('fs');
const { chromium } = require('playwright');
const { marked } = require('marked');

// Configure marked to preserve LaTeX math (\[ ... \] and \( ... \))
marked.setOptions({
    breaks: true,
    gfm: true,
});

// Read markdown file
const mdContent = fs.readFileSync('PROJECT_REPORT.md', 'utf-8');

// Convert markdown to HTML
const htmlBody = marked(mdContent);

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
        h1, h2, h3 { page-break-after: avoid; }
        img { max-width: 100%; height: auto; page-break-inside: avoid; margin: 10px 0; }
        pre { page-break-inside: avoid; overflow-x: auto; background-color: #f4f4f4; padding: 10px; }
        code { font-family: 'Courier New', monospace; background-color: #f4f4f4; padding: 2px 4px; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        blockquote { border-left: 4px solid #ddd; margin-left: 0; padding-left: 20px; }
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
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }
        };
    </script>
</head>
<body>
${htmlBody}
</body>
</html>`;

async function convertToPdf() {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    // Write HTML to temp file for debugging
    fs.writeFileSync('temp.html', htmlContent);
    
    await page.setContent(htmlContent, { waitUntil: 'domcontentloaded' });
    
    // Wait for MathJax to render
    await page.waitForFunction(() => {
        return window.MathJax && window.MathJax.startup && window.MathJax.startup.document && window.MathJax.startup.document.state() === 0;
    }, { timeout: 10000 }).catch(() => {
        console.log('Waiting for MathJax...');
    });
    
    // Additional wait to ensure rendering is complete
    await page.waitForTimeout(3000);
    
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

convertToPdf().catch(console.error);

