# This file is part of the Markdown to HTML converter project. It provides functions to convert inline markdown syntax to HTML. 

import re

def markdown_to_html_inline(text):
    """
    Converts inline markdown in the given text to HTML.
    Supports: **bold**, __bold__, *italic*, _italic_, `code`, [link](url), ![img](src)
    
    :param text: markdown text to convert, already configured with beginning conversions.
    :return: converted HTML string
    """
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold with **.
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
    # Bold with __.
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
    # Italic with *.
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    # Italic with _.
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    # Images with optional title
    def repl_image(match):
        alt_text = match.group(1)
        src = match.group(2)
        title = match.group(3)
        if title:
            return f'<img alt="{alt_text}" src="{src}" title="{title}">'
        else:
            return f'<img alt="{alt_text}" src="{src}">' 

    text = re.sub(r'!\[([^\]]*)\]\(([^\s)]+)(?:\s+"([^"]+)")?\)', repl_image, text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

# Test the inline conversion function.
def main():
    markdown_text = "This is **bold**, __more bold__, *italic*, _more italic_, `inline code`, [link](http://example.com), and ![image](http://example.com/image.png)."
    html_output = markdown_to_html_inline(markdown_text)
    print(html_output)
if __name__ == "__main__":
    main()