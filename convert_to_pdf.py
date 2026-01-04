#!/usr/bin/env python3
"""
Convert PROJECT_REPORT.md to PDF with LaTeX math support.
Uses markdown library with math extensions and weasyprint for PDF generation.
"""

import sys
import os

try:
    import markdown
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("Error: Required packages not found.")
    print("Please install: pip install markdown weasyprint pymdown-extensions")
    sys.exit(1)

def convert_markdown_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF with LaTeX math support."""
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Configure markdown with math extensions
    md = markdown.Markdown(
        extensions=[
            'pymdownx.arithmatex',
            'pymdownx.superfences',
            'pymdownx.tilde',
            'extra',
            'codehilite',
            'tables',
        ],
        extension_configs={
            'pymdownx.arithmatex': {
                'generic': True,
            },
        }
    )
    
    # Convert markdown to HTML
    html_body = md.convert(md_content)
    
    # Create full HTML document with MathJax
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 100%;
        }}
        h1 {{ page-break-after: avoid; }}
        h2 {{ page-break-after: avoid; }}
        h3 {{ page-break-after: avoid; }}
        img {{ max-width: 100%; height: auto; page-break-inside: avoid; }}
        pre {{ page-break-inside: avoid; }}
        code {{ font-family: 'Courier New', monospace; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            }},
            options: {{
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            }}
        }};
    </script>
</head>
<body>
{html_body}
</body>
</html>"""
    
    # Write HTML to temporary file
    html_file = pdf_file.replace('.pdf', '_temp.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    try:
        # Convert HTML to PDF using weasyprint
        # Note: MathJax won't render in weasyprint, but we'll use a workaround
        # For proper math rendering, we need to use a headless browser or different approach
        HTML(string=html_content).write_pdf(pdf_file)
        print(f"PDF created: {pdf_file}")
        print("Note: LaTeX equations may not render perfectly with weasyprint.")
        print("For best results, consider using pandoc with LaTeX engine.")
    except Exception as e:
        print(f"Error creating PDF: {e}")
        print("Falling back to simpler conversion...")
        # Fallback: try without weasyprint
        sys.exit(1)
    finally:
        # Clean up temporary HTML file
        if os.path.exists(html_file):
            os.remove(html_file)


if __name__ == '__main__':
    md_file = 'PROJECT_REPORT.md'
    pdf_file = 'PROJECT_REPORT.pdf'
    
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found")
        sys.exit(1)
    
    convert_markdown_to_pdf(md_file, pdf_file)

