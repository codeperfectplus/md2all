#!/usr/bin/env python3

import argparse
from md2all import convert_markdown

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Convert Markdown to HTML or PDF.")
    
    # Add arguments to the parser
    parser.add_argument("-m", "--md_path", type=str, help="Path to the Markdown file to convert.")
    parser.add_argument("-f", "--format", choices=["html", "pdf"], help="Output format: html or pdf. Default is 'pdf'.")
    parser.add_argument("-o", "--output_dir", default="", help="*(Optional)* Directory to save the converted file. Defaults to input file's directory.")
    parser.add_argument("-c", "--use_cdn", action="store_true", default=False, help="*(Optional)* If True, uses CDN else uses offline resources. Default is False.")

    # Parse the arguments
    args = parser.parse_args()

    # Convert Markdown based on the output format argument
    if args.format == "html":
        print(f"Converting {args.md_path} to HTML...")
        output_path = convert_markdown(args.md_path, output_dir=args.output_dir, use_cdn=args.use_cdn)
        print(f"Conversion to HTML completed. Output saved in {output_path}")
    elif args.format == "pdf":
        print(f"Converting {args.md_path} to PDF...")
        output_path = convert_markdown(args.md_path, output_dir=args.output_dir, use_cdn=args.use_cdn, output_format="pdf")
        print(f"Conversion to PDF completed. Output saved in {output_path}")

if __name__ == "__main__":
    main()
