from md2all import convert_markdown

path = "/home/admin/Documents/html_convertor/test.md"
print("Converting markdown to HTML...")
html = convert_markdown(path, use_cdn=True, output_format="pdf")
print("Saving HTML to file...", html)