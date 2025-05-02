import os
import shutil
import re
from pathlib import Path

import markdown
from bs4 import BeautifulSoup

class MarkdownConverter:
    """
    A class to convert Markdown text to HTML. 
    Includes optional MathJax, Tailwind CSS, and custom CSS handling.
    By default, libraries are stored in ~/.lib, but this can be overridden.
    """

    def __init__(self, lib_dir: str = ""):
        # Set lib_dir to ~/.lib if not provided
        if not lib_dir:
            home_dir = os.path.expanduser("~")
            lib_dir = os.path.join(home_dir, ".lib")
        self.lib_dir = lib_dir

        # Paths to library files (MathJax, custom CSS, Tailwind)
        self.root_dir = Path(__file__).resolve().parent
        self.source_mathjax_js = os.path.join(self.root_dir, "libs", "tex-mml-chtml.js")
        self.source_custom_css = os.path.join(self.root_dir, "libs", "custom_css.css")
        self.source_tailwind_path = os.path.join(self.root_dir, "libs", "tailwind.min.css")

    async def _setup_directory(self, directory: str):
        """Ensure the directory exists asynchronously."""
        os.makedirs(directory, exist_ok=True)

    async def _copy_file(self, src: str):
        """Copy a file from src to dst if it doesn't already exist asynchronously."""
        dst = os.path.join(self.lib_dir, os.path.basename(src))
        src = os.path.normpath(src)
        dst = os.path.normpath(dst)
        if not os.path.exists(src):
            raise FileNotFoundError(f"Source file {src} does not exist.")
        if os.path.exists(dst):
            return dst
        shutil.copy2(src, dst)
        return dst

    async def _setup_mathjax(self):
        """Setup MathJax by copying it to the centralized directory asynchronously."""
        await self._setup_directory(self.lib_dir)
        dst_path = await self._copy_file(self.source_mathjax_js)
        return dst_path

    async def _setup_custom_css(self):
        """Setup the custom CSS by copying it to the centralized directory asynchronously."""
        dst_path = await self._copy_file(self.source_custom_css)
        return dst_path

    async def _setup_tailwind(self):
        """Setup the Tailwind CSS by copying it to the centralized directory asynchronously."""
        dst_path = await self._copy_file(self.source_tailwind_path)
        return dst_path

    async def _modify_classes(self, html_content: str) -> str:
        """Modify HTML content asynchronously by injecting Tailwind classes into elements."""
        soup = BeautifulSoup(html_content, 'html.parser')

        tag_class_map = {
            'h1': "text-4xl font-bold mt-4 mb-2",
            'h2': "text-4xl font-semibold mt-4 mb-2",
            'h3': "text-2xl font-medium mt-4 mb-2",
            'h4': "text-xl font-medium mt-4 mb-2",
            'p': "text-base leading-relaxed mt-2 mb-4",
            'code': "bg-gray-100 p-1 rounded-md",
            'pre': "bg-gray-900 text-white p-4 rounded-md overflow-x-auto",
        }

        for tag, tailwind_classes in tag_class_map.items():
            for element in soup.find_all(tag):
                existing_classes = element.get("class", [])
                new_classes = tailwind_classes.split()
                combined_classes = list(set(existing_classes + new_classes))
                element['class'] = combined_classes

        return str(soup)

    async def _convert_latex_format(self, text: str) -> str:
        """
        Convert LaTeX math syntax to HTML-compatible format asynchronously 
        by replacing delimiters with custom tags or spans.
        """
        text = re.sub(r'\\\[(.*?)\\\]', r'<div class="latex-display">\1</div>', text, flags=re.DOTALL)
        text = re.sub(r'\\\((.*?)\\\)', r'<span class="latex-inline">\1</span>', text, flags=re.DOTALL)
        return text

    async def convert_markdown_to_html_async(self, markdown_text: str, use_cdn: bool = False) -> str:
        """
        Convert Markdown text to HTML. 
        If use_cdn is True, loads MathJax and Tailwind from CDN instead of copying local libs.
        Returns the final HTML as a string.
        """
        if not markdown_text.strip():
            raise ValueError("Markdown text is empty or invalid.")

        markdown_text = await self._convert_latex_format(markdown_text)

        # Convert the Markdown text to HTML
        html_content = markdown.markdown(
            markdown_text,
            extensions=['md_in_html', 'fenced_code', 'codehilite', 'toc', 'attr_list', 'tables']
        )
        html_content = await self._modify_classes(html_content)

        if use_cdn:
            html_block = """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
                    onload="renderMathInElement(document.body);"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@3.2.7/dist/tailwind.min.css">
            <style>
                /* A basic default custom CSS placeholder if needed. */
            </style>
            """
        else:
            mathjax_path = Path(await self._setup_mathjax()).resolve().as_uri()
            tailwind_path = Path(await self._setup_tailwind()).resolve().as_uri()
            custom_css_path = Path(await self._setup_custom_css()).resolve().as_uri()

            html_block = f'''
            <script type="text/javascript" id="MathJax-script" async src="{mathjax_path}"></script>
            <link href="{tailwind_path}" rel="stylesheet">
            <link rel="stylesheet" href="{custom_css_path}" />
            '''

        # Build the final HTML with a minimal template
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en" class="scroll-smooth bg-gray-50 text-gray-900 antialiased">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Markdown to HTML</title>
                {html_block}
            </head>
            <body for="html-export" class="min-h-screen flex flex-col justify-between">
                <main class="flex-1">
                    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 prose prose-lg prose-slate">
                        {html_content}
                    </div>
                </main>
            </body>
        </html>
        """

        return html_template

    def convert_markdown_to_html(self, markdown_text: str, use_cdn: bool = False) -> str:
        """
        Synchronous wrapper around the async method to convert Markdown to HTML.
        """
        import asyncio
        return asyncio.run(self.convert_markdown_to_html_async(markdown_text, use_cdn))