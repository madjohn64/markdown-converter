# In an experiment with GitHub Copilot, I used it directly to write this code.
# This script converts a Markdown file to HTML using a custom MarkdownConverter class, which I wrote in a separate file named `converter.py`.
# The only correction that I had to make was to add the import statement for the `MarkdownConverter` class and update the converter usage below.

import sys
import os
from converter import MarkdownConverter

def main():
    if len(sys.argv) != 3:
        print("Usage: python run.py <input_markdown_file> <output_html_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' does not exist.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    converter = MarkdownConverter()
    html_text = converter.convert(markdown_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_text)

    print(f"Converted '{input_file}' to '{output_file}' successfully.")

if __name__ == "__main__":
    main()