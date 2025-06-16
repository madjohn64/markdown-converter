import re
from md2html import Token

markdown = """
An h2 header
---------

An h1 header
=====

Now a nested list:

 1. First, get these ingredients:

      * carrots
      * celery
      * lentils


 2. Boil some water.
 [image] Water boiling.
 `code goes here`
"""
tokens = []
i = 0 
markdown_lines = markdown.splitlines()
print(markdown_lines)       
while i < len(markdown_lines):
    line = markdown_lines[i].rstrip()
    if not line.strip() :
        print("Empty Line")
        tokens.append(Token('EMPTY_LINE', ''))
        i += 1
        continue
    
    # Headers 1 & 2 - underline type
    if i < len(markdown_lines) - 1 and re.match(r"^[#`-]|^\*|^\d|^\[|^\!", line) == None and re.match(r"^=|^-", markdown_lines[i + 1]) != None :
        print("Header")
        if markdown_lines[i + 1].startswith("=") :
            tokens.append(Token(f'HEADER_1', line))
        else : tokens.append(Token(f'HEADER_2', line))
        i += 1
        continue
    
    else : i += 1

print(tokens)