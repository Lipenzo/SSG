from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = 'Unordered_list'
    ORDERED_LIST = "Ordered_list"
    
def block_to_html_type(block):
    heading_pattern = r"^#{1,6} .*"
    code_pattern = r"^```(.*\n?)*```$"
    quote_pattern = r"^(>.*\n)*>.*$"
    unorlist_pattern = r"^([\*-] .*\n)*[\*-] .*$"
    orlistline_pattern = r"\d+. "
    if re.search(heading_pattern, block) != None:
        return BlockType.HEADING
    if re.search(code_pattern, block) != None:
        return BlockType.CODE
    if re.search(quote_pattern, block) != None:
        return BlockType.QUOTE
    if re.search(unorlist_pattern, block) != None:
        return BlockType.UNORDERED_LIST
    lines = block.splitlines(True)
    ordered_list = True
    for i in range(len(lines)):
        line_start = re.search(orlistline_pattern, lines[i])
        if line_start == None or line_start[0] != f"{i+1}. ":
            ordered_list = False
            break
    if ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

