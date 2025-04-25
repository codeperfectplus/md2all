import os
from mdconvertor_tools import transform

md_path = "test.md"
transform(md_path, output_format="html")
