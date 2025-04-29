import os
import shutil
import markdown
import re
import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
import aiofiles
from md2all.utils import html_to_pdf_with_playwright, ensure_playwright_installed

ROOT_DIR = Path(__file__).resolve().parent
home_dir = os.path.expanduser("~")
lib_dir = os.path.join(home_dir, ".lib")

source_mathjax_js = os.path.join(ROOT_DIR, "libs", "tex-mml-chtml.js")
source_custom_css = os.path.join(ROOT_DIR, "libs", "custom_css.css")
source_tailwind_path = os.path.join(ROOT_DIR, "libs", "tailwind.min.css")


async def setup_directory(directory):
    """Ensure the directory exists asynchronously."""
    os.makedirs(directory, exist_ok=True)

async def copy_file(src):
    """Copy a file from src to dst if it doesn't already exist asynchronously."""
    dst = os.path.join(lib_dir, os.path.basename(src))
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source file {src} does not exist.")
    if os.path.exists(dst):
        return dst
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
    return dst

async def setup_mathjax():
    """Setup MathJax by copying it to the centralized directory asynchronously."""
    await setup_directory(lib_dir)
    dst_path = await copy_file(source_mathjax_js)
    return dst_path

async def setup_custom_css():
    """Setup the custom CSS by copying it to the centralized directory asynchronously."""
    dst_path = await copy_file(source_custom_css)
    return dst_path

async def setup_tailwind():
    """Setup the Tailwind CSS by copying it to the centralized directory asynchronously."""
    dst_path = await copy_file(source_tailwind_path)
    return dst_path

async def modify_classes(html_content):
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

async def convert_latex_format(text):
    """Convert LaTeX math syntax to Markdown format asynchronously and add custom CSS classes."""    
    text = re.sub(r'\\\[(.*?)\\\]', r'<div class="latex-display">\1</div>', text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', r'<span class="latex-inline">\1</span>', text, flags=re.DOTALL)
    return text

async def read_markdown_file(file_path):
    """Read the content of a markdown file asynchronously."""
    async with aiofiles.open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return await f.read()

async def convert_markdown_async(md_path: str, output_dir: str = "", output_format : str = "html", use_cdn: bool = False) -> str:
    """Convert Markdown to HTML (optionally PDF) asynchronously, save results in appropriate location."""
    if not md_path:
        raise ValueError("Markdown file path cannot be empty. Please provide a valid .md file path.")

    # get full path if not absolute
    if not os.path.isabs(md_path):
        md_path = os.path.abspath(md_path)
    
    markdown_text = await read_markdown_file(md_path)
    markdown_text = await convert_latex_format(markdown_text)

    # Prepare file names and paths
    base_name = os.path.basename(md_path).replace(".md", "")
    os.makedirs
    temp_html_path = os.path.join("/tmp", f"{base_name}.html")

    if output_dir == "":
        output_dir = os.path.dirname(md_path)

    final_output_path = os.path.join(output_dir, f"{base_name}.{output_format}") if output_dir else md_path.replace(".md", f".{output_format}")
    print(f"Final output path: {final_output_path}")

    # Convert to HTML content
    html_content = markdown.markdown(
        markdown_text,
        extensions=['md_in_html', 'fenced_code', 'codehilite', 'toc', 'attr_list', 'tables']
    )
    html_content = await modify_classes(html_content)

    if use_cdn:
        html_block = """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
                onload="renderMathInElement(document.body);"></script>
        """
    else:
        html_block = f'''<script type="text/javascript" id="MathJax-script" async src="{Path(await setup_mathjax()).as_uri()}"></script>
        <link href="{Path(await setup_tailwind()).as_uri()}" rel="stylesheet">
        <link rel="stylesheet" href="{Path(await setup_custom_css()).as_uri()}" />
        '''

    # Inject into template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en" class="scroll-smooth bg-gray-50 text-gray-900 antialiased">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{base_name}</title>
            <link href="{Path(await setup_tailwind()).as_uri()}" rel="stylesheet">
            <link rel="stylesheet" href="{Path(await setup_custom_css()).as_uri()}" />
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

    # Save temporary HTML to /tmp
    async with aiofiles.open(temp_html_path, "w", encoding="utf-8") as f:
        await f.write(html_template)

    # If output format is .html, copy to output directory
    if output_format == "html":
        await setup_directory(output_dir)
        shutil.copy(temp_html_path, final_output_path)

    # If output format is .pdf, delegate to PDF converter
    elif output_format == "pdf":
        await setup_directory(output_dir)
        await ensure_playwright_installed()
        await html_to_pdf_with_playwright(temp_html_path, final_output_path)

    return final_output_path  # Optional: return for chaining or logging

def convert_markdown(md_path: str, output_dir: str = "", output_format: str = "html", use_cdn: bool = False) -> str:
    """Convert Markdown to HTML (optionally PDF), save results in appropriate location."""
    return asyncio.run(convert_markdown_async(md_path, output_dir, output_format, use_cdn))