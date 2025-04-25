import os
import shutil
import markdown
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent
print("Root Directory:", ROOT_DIR)
# Get full path to user's home and centralized .lib directory
home_dir = os.path.expanduser("~")
lib_dir = os.path.join(home_dir, ".lib")

source_mathjax_js = os.path.join(ROOT_DIR, "libs", "tex-mml-chtml.js")
source_custom_css = os.path.join(ROOT_DIR, "libs", "custom_css.css")
source_tailwind_path = os.path.join(ROOT_DIR, "libs", "tailwind.min.css")

def setup_directory(directory):
    """Ensure the directory exists."""
    os.makedirs(directory, exist_ok=True)

def copy_file(src):
    """Copy a file from src to dst if it doesn't already exist."""
    dst = os.path.join(lib_dir, os.path.basename(src))
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)
    # Check if the source file exists
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source file {src} does not exist.")    
    if os.path.exists(dst):
        return dst
            
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
    return dst

def setup_mathjax():
    """Setup MathJax by copying it to the centralized directory."""
    setup_directory(lib_dir)
    dst_path = copy_file(source_mathjax_js)
    return dst_path

def setup_custom_css():
    """Setup the custom CSS by copying it to the centralized directory."""
    dst_path = copy_file(source_custom_css)
    return dst_path

def setup_tailwind():
    """Setup the Tailwind CSS by copying it to the centralized directory."""
    dst_path = copy_file(source_tailwind_path)
    return dst_path

from bs4 import BeautifulSoup

def modify_classes(html_content):
    """Modify HTML content by injecting Tailwind classes into elements using BeautifulSoup."""
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

def convert_latex_format(text):
    """Convert LaTeX math syntax to Markdown format and add custom CSS classes."""    
    text = re.sub(r'\\\[(.*?)\\\]', r'<div class="latex-display">\1</div>', text, flags=re.DOTALL)
    # Convert inline LaTeX (inline math) to a span with a custom class
    text = re.sub(r'\\\((.*?)\\\)', r'<span class="latex-inline">\1</span>', text, flags=re.DOTALL)
    
    return text

def read_markdown_file(file_path):
    """Read the content of a markdown file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def transform(md_path, output_dir="", output_format=""):
    """Convert Markdown text to HTML with Tailwind CSS classes and MathJax setup."""
    print("Processing Markdown file:", md_path)
    markdown_text = read_markdown_file(md_path)
    markdown_text = convert_latex_format(markdown_text)

    if output_dir:
        setup_directory(output_dir)
        output_dir = os.path.join(output_dir, os.path.basename(md_path).replace(".md", f".{output_format}"))
    else:
        output_dir = md_path.replace(".md", f".{output_format}")

    html_content = markdown.markdown(markdown_text, extensions=['md_in_html', 'fenced_code', 'codehilite', 'toc', 'attr_list'])
    html_content = modify_classes(html_content)
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en" class="scroll-smooth bg-gray-50 text-gray-900 antialiased">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>{title}</title>

            <!-- Tailwind CSS -->
            <link href="{centralized_tailwind_path}" rel="stylesheet">

            <!-- MathJax -->
            <script type="text/javascript" id="MathJax-script" async
                src="{centralized_mathjax_path}"></script>

            <!-- Custom CSS -->
            <link rel="stylesheet" href="{centralized_css_path}" />
        </head>
        <body for="html-export" class="min-h-screen flex flex-col justify-between">

            <!-- Main content -->
            <main class="flex-1">
                <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 prose prose-lg prose-slate">
                    {html_content}
                </div>
            </main>    
        </body>
    </html>
    """
    
    html_template = html_template.replace("{title}", "Markdown to HTML Conversion")
    html_template = html_template.replace("{html_content}", html_content)
    html_template = html_template.replace("{centralized_mathjax_path}", Path(setup_mathjax()).as_uri())
    html_template = html_template.replace("{centralized_css_path}", Path(setup_custom_css()).as_uri())
    html_template = html_template.replace("{centralized_tailwind_path}", Path(setup_tailwind()).as_uri())

    
    with open(output_dir, "w", encoding="utf-8") as f:
        f.write(html_template)
