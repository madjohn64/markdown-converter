# Central logic for Markdown converstion to HTML.

import re
from typing import List, Tuple

class Token:
    def __init__(self, type_, content):
        self.type = type_
        self.content = content

    def __repr__(self):
        return f"Token(type={self.type}, content={self.content!r})"

class MarkdownConverter :
    """
    Core converter class for Markdown conversion. 
    
    Class does not include the processing of files. This is handled separately. 
    """
    
    def __init__(self, *, extensions=None, output_format = "html5") :
        """
        Initialize the converter.

        :param extensions: list of markdown extensions to enable
        :param output_format: output format for HTML (html5 or xhtml1)
        """        
        self.extensions = extensions
        self.output_format = output_format
    
    def headerConvert(self, header_text: str) -> str :
        """
        convert function determined this is a header. This parses what level and 
        converts to html.

        :param header_text: raw markdown string
        :return: converted HTML string
        """
        header_text = header_text.strip()
        headerCount = 0
        for char in header_text :
            if char == '#' : 
                headerCount += 1
                
            else :
                header_text = header_text[headerCount:].strip()
                break
        if headerCount > 6 : headerCount = 6
        return "<h" + str(headerCount) + ">" + header_text + "</h" + str(headerCount) + ">" + "\n"
    
    def blockquoteConvert(self, quote_text: str) -> str :
        """
        convert function determined this is a blockquote. This converts it to html.
        
        :param quote_text: raw markdown string
        :return: converted HTML string
        """
        return "<blockquote>" + quote_text.strip() + "</blockquote> \n"
    
    def orderedListConvert(self, text: str) -> str :
        """
        Convert function determined this markdown text is an ordered list member. 
        This converts it to html.
        
        :param quote_text: raw markdown string
        :return: converted HTML string
        """
        html_output = ""
        for line in text.splitlines() :
            html_output = html_output + "\t<li>" + line.strip() + "</li>\n"
        return "<ol>\n" + html_output + "</ol>"
 
 #Commenting out tokenize. Will erase once no longer needed as a reference.
    """   
    def tokenize(self, markdown_lines: List[str]) -> List[Tuple] :
        """
        #convert list of lines into tokens, categorizing them.
        
        #:param markdown_list: list of strings in markdown format
        #:return tokens: List of Tokens 
    """
        tokens = []        
        while i < len(markdown_lines):
            line = markdown_lines[i].rstrip()
            if not line.strip():
                tokens.append(Token('EMPTY_LINE', ''))
                i += 1
                continue

            # Headers - baseline
            if re.match(r'^(#{1,6})+(.*)', line):
                m = re.match(r'^(#{1,6})+(.*)', line)
                level = len(m.group(1))
                content = m.group(2)
                tokens.append(Token(f'HEADER_{level}', content))
                i += 1
                continue
            
            # Headers 1 & 2 - underline type
            if i < len(markdown_lines) - 1 and re.match(r"^[#`-]|^\*|^\d|^\[|^\!", line) == None and re.match(r"^=|^-", markdown_lines[i + 1]) != None :
                if markdown_lines[i + 1].startswith("=") :
                    tokens.append(Token(f'HEADER_1', line))
                else : tokens.append(Token(f'HEADER_2', line))
    """
    
    def convert(self, markdown_text: str) -> str :
        """
        Break down text by lines. 
        Hand list of lines to tokenizer to construct tokens. 
        Receives token_dict back from tokenizer. 
        Use token categories to hand each token to respective 
        Convert markdown text to HTML.

        :param markdown_text: raw markdown string
        :return: converted HTML string
        """
        htmlText = ''
        lines = markdown_text.split("\n")
        i = 0
        while i < len(lines) :
            line = lines[i].rstrip()
            
            if not line.strip() : #Skip empty lines.
                i += 1
                continue 
            
            # Standard Headers with '#' beginning. Passes the '#' without stripping.
            if line.startswith('#') : 
                htmlText = htmlText + self.headerConvert(line)
                i += 1
                continue
            
            # Headers (H1 and H2 type) based on Underlines. 
            if i < len(lines) - 1 and re.match(r"^[#`-]|^\*|^\d|^\[|^\!", line) == None and re.match(r"^==|^--", lines[i + 1]) != None :
                if lines[i + 1].startswith("=") :
                    htmlText = htmlText + self.headerConvert("#" + line) #Allows use of the same Header function.
                if lines[i + 1].startswith("-") :
                    htmlText = htmlText + self.headerConvert("##" + line)
                i += 2 #Increase two to skip the line that underlines since this is not part of the html.
                continue
                    
            # Blockquote
            if line.startswith('>') or line.startswith(' >') :
                quote = line.strip().strip('>')
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('>') : 
                    quote = quote + '\n' + lines[j].strip().lstrip('>')
                    j += 1
                htmlText = htmlText + self.blockquoteConvert(quote)
                i += max(1, j-i)
                continue
            
            #Ordered List.
            # DOESN'T WORK - NEED TO FIX.
            if re.match(r"^\d*\.", line) != None :
                quote = re.sub(r"^\d*\.", "", line.strip())
                j = i + 1
                while j < len(lines) and re.match(r"^\d*\.", lines[j]) != None : 
                    quote = quote + "\n" + re.sub(r"^\d*\.", "", lines[j].strip())
                    j += 1
                htmlText = htmlText + self.orderedListConvert(quote)
                i += max(1, j-i)
                continue
            
            # Paragraph catch all. Needs to check for next lines - INCOMPLETE.
            htmlText = htmlText + "<p>" + line + "</p>\n"
            i += 1
                   
        return htmlText
                
        


#Test Driver - delete this once complete.
converter = MarkdownConverter()

html_output = converter.convert("# Hello World")
print(html_output)

html_output = converter.convert("Hello World\n------\n### Hello Again!!")
print(html_output)

html_output = converter.convert("#### Hello World")
print(html_output)

html_output = converter.convert("#### Hello World\n\n>This is a block quote. \n >And it's going still.\n>And going.\n1. This is a OL.\n2. Item 2.\n300. Item 3.")
print(html_output)
