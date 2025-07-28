# Central logic for Markdown conversion to HTML.
# This file is part of the Markdown to HTML converter project. It provides the core logic for converting Markdown syntax to HTML.

import re, html
from typing import List, Tuple
from . import inlineConvert  # Importing inline conversion function.

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
        return "<ol>\n" + html_output + "</ol>\n"
    
    def unorderedListConvert(self, text: str, sub_list: bool) -> str :
        """
        Convert function determined this markdown text is an unordered list member. 
        This converts it to html.
        
        :param quote_text: raw markdown string
        :return: converted HTML string
        """
        html_output = ""
        if sub_list : 
            for line in text.splitlines() :
                html_output = html_output + "\t\t<li>" + line.strip() + "</li>\n"
        else :
            for line in text.splitlines() :
                if re.match(r"^<li>|<ul>", line.strip()) == None :
                    html_output = html_output + "\t<li>" + line.strip() + "</li>\n"
        return "<ul>\n" + html_output + "</ul>\n"

    def codeBlockConvert(self, code_block: str) -> str :
        """
        Convert function determined this markdown text is a code block. 
        This converts the code block to html.
        
        :param code_block: raw markdown string
        :return: converted HTML string
        """
        html_lines = ['\t' + line for line in code_block.splitlines()]
        html_code = '\n'.join(html_lines)
        return f"<pre><code>\n{html.escape(html_code)}\n</code></pre>\n"
    
    def inlineCodeConvert(self, code_text: str) -> str :
        """
        Convert function determined this markdown text is inline code. 
        This converts the inline code to html.
        
        :param code_text: raw markdown string
        :return: converted HTML string
        """
        return f"<code>{html.escape(code_text.strip())}</code>"
    
    def markdown_table_to_html(self, table_lines: List[str]) -> str:
        """
        Converts a list of Markdown table lines to an HTML table string.
        """
        # Remove leading/trailing whitespace and filter out empty lines
        stripped_lines = []
        for line in table_lines:
            stripped = line.strip()
            if stripped:
                stripped_lines.append(stripped)
        table_lines = stripped_lines
        if len(table_lines) < 2:
            return ""  # Not a valid table

        # Split header and separator
        header = table_lines[0]
        separator = table_lines[1]
        rows = table_lines[2:]

        # Split columns by '|', ignoring leading/trailing pipes
        def split_row(row: str) -> List[str]:
            return [cell.strip() for cell in row.strip('|').split('|')]

        header_cells = split_row(header)
        html = ['<table>', '  <thead>', '    <tr>']
        for cell in header_cells:
            html.append(f'      <th>{cell}</th>')
        html.extend(['    </tr>', '  </thead>', '  <tbody>'])

        for row in rows:
            if not row.strip():
                continue
            cells = split_row(row)
            html.append('    <tr>')
            for cell in cells:
                html.append(f'      <td>{cell}</td>')
            html.append('    </tr>')

        html.extend(['  </tbody>', '</table>'])
        return '\n'.join(html)
    
    def convert(self, markdown_text: str) -> str :
        """
        Parse the Markdown text and convert it to HTML.

        The input is split into lines and each line is inspected in order
        to recognise block level structures such as headers, lists,
        block quotes, horizontal rules and tables.  Matching lines are
        converted to their HTML counterparts immediately.  Once all lines
        have been processed the resulting HTML string is passed to the
        inline converter so that elements like **bold**, *italic*, links
        and inline code are handled.

        :param markdown_text: raw markdown string
        :return: converted HTML string
        """
        htmlText = ''
        lines = markdown_text.split("\n")
        i = 0
        while i < len(lines) :
            line = lines[i].rstrip()
            
            if not line.strip() : #Skip empty lines in HTML, but keep them for code formatting.
                htmlText += "\n"
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
            
            # Code Blocks. Doesn't work properly.
            """
            if re.match(r"^\s*```|\t)", line):
                code_block_lines = [re.sub(r"^( {4}|\t)", "", line)]
                j = i + 1
                while j < len(lines) and re.match(r"^( {4}|\t)", lines[j]):
                    code_block_lines.append(re.sub(r"^( {4}|\t)", "", lines[j]))
                    j += 1
                code_block = "\n".join(code_block_lines)
                htmlText += self.codeBlockConvert(code_block)
                i = j
                continue"""
                    
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
            
            # Horizontal Rule.
            if re.match(r"^[-*]{3,}|^_+$", line) != None :
                htmlText = htmlText + "<hr>\n"
                i += 1
                continue
            
            #Ordered List.
            if re.match(r"^\s*\d+\.", line) != None :
                ordList = re.sub(r"^\d*\.", "", line.strip())
                j = i + 1
                while j < len(lines) and re.match(r"\s*^\d*\.", lines[j]) != None : 
                    ordList = ordList + "\n" + re.sub(r"^\d*\.", "", lines[j].strip())
                    j += 1
                htmlText = htmlText + self.orderedListConvert(ordList)
                i += max(1, j-i)
                continue
            
            #Unordered List.
            if re.match(r"^\s*\*\s|\s*-\s|\s*\+\s", line.strip()) != None :
                unOrdList = re.sub(r"^\*\s|-\s|\+\s", "", line.strip())
                subList = ""
                j = i + 1
                while j < len(lines) and (re.match(r"^\*\s|-\s|\+\s", lines[j].strip()) != None ) : 
                    if re.match(r"^\t\*\s|\t-\s|\t\+\s", lines[j]) != None :
                        subList = subList + re.sub(r"^\t\*\s|\t-\s|\t\+\s", "", lines[j].strip()) + "\n"
                    else :
                        if subList != "" :
                            unOrdList = unOrdList + "\n" + self.unorderedListConvert(subList, True) 
                            subList = ""
                        unOrdList = unOrdList + "\n" + re.sub(r"^\*\s|-\s|\+\s", "", lines[j].strip())
                    j += 1
                htmlText = htmlText + self.unorderedListConvert(unOrdList, False)
                i += max(1, j-i)
                continue
            
            # Tables
            if (
                '|' in line and
                i + 1 < len(lines) and
                re.match(r'^\s*\|?[\s:-]+\|[\s|:-]*$', lines[i + 1])
            ):
                # Collect all table lines
                table_lines = [line]
                i += 1
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                htmlText += self.markdown_table_to_html(table_lines) + '\n'
                continue  # Skip incrementing i at the end of the loop
            
            # Paragraph catch all. Needs to check for next lines - INCOMPLETE.
            htmlText = htmlText + "<p>" + line + "</p>\n"
            i += 1
            
            htmlText = inlineConvert.markdown_to_html_inline(htmlText)  # Convert inline markdown to HTML.
                   
        return htmlText

#Test Driver - delete this once complete.
def main() :
    """
    Test driver for the MarkdownConverter class.
    """
    
    converter = MarkdownConverter()

    html_output = converter.convert("# Hello World")
    print(html_output)

    html_output = converter.convert("Hello World\n------\n### Hello Again!!")
    print(html_output)

    html_output = converter.convert("#### Hello World")
    print(html_output)

    html_output = converter.convert("#### Hello World\n\n>This is a block quote. \n >And it's going still.\n>And going.\n1. This is a OL.\n2. Item 2.\n300. Item 3.\n- Unordered List.\n- Item 2.\n- Item 3.\n* Item 4.\n* Item 5.\n\nThis is a paragraph.\n\n")
    print(html_output)

    html_output = converter.convert("\n\t<tag>This is a code block.\n\tWith some code in it.</tag>\n")
    print(html_output)

    html_output = converter.convert("| Integrate symbolic reasoning, causal inference, or explainable AI techniques                       | Causal machine learning for healthcare or policy applications    |\n| **Domain-Specific AI Applications**              | Focus on AI in specialized sectors such as healthcare, law, art, or finance                        | Computer vision in radiology, generative AI in art/animation     |\n| **User-Centered/Participatory AI**               | Design research with end-user input; focus on human-AI interaction           | Human-centered design in assistive robotics or educational tools |\n\n---\n\n## **Summary Table**\n\n| Step                       | Actions               |\n|----------------------------|---------------------------------------------------------------------|\n| Build & Specialize Skills  | Master core AI topics, explore interdisciplinary learning, publish  |\n| Network Widely             | Engage at conferences, join multi-field groups, active online       |\n| Apply Broadly              | Seek roles in classic and adjacent disciplines, tailor applications |\n| Iterate & Expand           | Seek feedback, grow skills (including across domains), share work   |\n| Explore Alternatives       | Collaborate and innovate with diverse methodologies and teams       |\n\n---\n\n**Tips:**\n- **Stay Curious:** Explore alternative research paradigms and seek unique insights from related fields.\n- **Broaden Horizons:** A flexible, interdisciplinary mindset often distinguishes top AI researchers.\n- **Persistence Counts:** The field is competitive, but creativity, adaptability, and networking multiply your chances for success.\n\n---\n\nLet me know if you want a **tailored plan** for a specific AI subfield or advice on integrating a particular discipline into your AI research career!")
    print(html_output)

if __name__ == "__main__":
    main()
