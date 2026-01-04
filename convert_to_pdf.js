const fs = require('fs');
const { chromium } = require('playwright');
const markdown = require('markdown-pdf');

// Read markdown file
const mdContent = fs.readFileSync('PROJECT_REPORT.md', 'utf-8');

// Create HTML with MathJax support
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
        img { max-width: 100%; height: auto; page-break-inside: avoid; }
        pre { page-break-inside: avoid; overflow-x: auto; }
        code { font-family: 'Courier New', monospace; background-color: #f4f4f4; padding: 2px 4px; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
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
${mdContent.split('\n').map(line => {
    // Simple markdown to HTML conversion (basic)
    // For full markdown support, use a markdown library
    return line;
}).join('\n')}
</body>
</html>`;

async function convertToPdf() {
    try {
        // Use markdown-pdf which might handle math better
        markdown().from('PROJECT_REPORT.md').to('PROJECT_REPORT.pdf', function () {
            console.log('PDF created with markdown-pdf');
        });
    } catch (error) {
        console.error('Error:', error);
        // Fallback to playwright
        const browser = await chromium.launch();
        const page = await browser.newPage();
        await page.setContent(htmlContent, { waitUntil: 'networkidle' });
        await page.waitForTimeout(3000); // Wait for MathJax to render
        await page.pdf({ path: 'PROJECT_REPORT.pdf', format: 'A4', margin: { top: '2cm', bottom: '2cm', left: '2cm', right: '2cm' } });
        await browser.close();
        console.log('PDF created with Playwright');
    }
}

convertToPdf();

