import os
from md2htmlify import MarkdownConverter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def convert_markdown_file_to_html(md_file_path: str, lib_directory: str = "") -> str:
    """
    Reads a Markdown file from the specified path, converts it to HTML using the MarkdownConverter,
    and returns the resulting HTML as a string.
    """
    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"The specified Markdown file was not found: {md_file_path}")

    # Read the markdown file
    with open(md_file_path, "r", encoding="utf-8") as md_file:
        markdown_text = md_file.read()

    # Create a MarkdownConverter object, optionally specifying a library directory for resources
    converter = MarkdownConverter(lib_dir=lib_directory)

    # Convert the markdown text to HTML
    html_output = converter.convert_markdown_to_html(markdown_text)
    return html_output

if __name__ == "__main__":
    # Example usage
    username = "user"

    test_md_path = os.path.join(ROOT_DIR, "test_data/test.md")
    lib_dir_path = f"/home/{username}/.lib"

    html_result = convert_markdown_file_to_html(test_md_path, lib_dir_path)
    print(html_result)