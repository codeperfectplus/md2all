from md2all import convert_markdown

md_path = "test_data/test.md"
convert_markdown(md_path, output_format="html")


md_path = "test_data/test.md"
convert_markdown(md_path, output_format="pdf")

