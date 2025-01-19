from htmlnode import HTMLNode
from leafnode import LeafNode
from block import BlockType, block_to_html_type
from utilities import markdown_to_blocks, text_to_text_nodes, text_to_node_html_node

def __get_children(block):
    leafnode_list = []
    nodes = text_to_text_nodes(block)
    for node in nodes:
        leafnode_list.append(text_to_node_html_node(node))
    return leafnode_list

def heading_block_to_leafnode(block):
    heading_level = f"h{len(block.split()[0])}"
    text = block.lstrip("#")[1:]
    children = __get_children(text)
    if len(children) == 1 and children[0].tag == None:
        return LeafNode(heading_level, children[0].value)
    return HTMLNode(heading_level, children=children)
    

def code_block_to_leafnode(block):
    return LeafNode("code", block[3:-3])

def quote_block_to_leafnode(block):
    new_block = ""
    for line in block.splitlines(True):
        new_block += line[2:]
    return LeafNode("blockquote", new_block)

def unorlist_block_to_HTMLNode(block):
    leafnode_list = []
    for line in block.splitlines():
        text = line[2:]
        children = __get_children(text)
        if len(children) == 1 and children[0].tag == None:
            leafnode_list.append(LeafNode("li", text))
        else:
            leafnode_list.append(HTMLNode("li", children=children))
    return HTMLNode("ul", children=leafnode_list)

def ordlist_block_to_HTMLNode(block):
    leafnode_list = []
    for line in block.splitlines():
        text = line[len(line.split()[0])+1:]
        children = __get_children(text)
        if len(children) == 1 and children[0].tag == None:
            leafnode_list.append(LeafNode("li", text))
        else:
            leafnode_list.append(HTMLNode("li", children=children))
    return HTMLNode("ol", children=leafnode_list)

def paragraph_block_to_HTMLNode(block):
    leafnode_list = __get_children(block)
    if len(leafnode_list) == 1:
        return leafnode_list[0]
    return HTMLNode("p", children=leafnode_list)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_html_type(block)
        if block_type == BlockType.HEADING:
            nodes.append(heading_block_to_leafnode(block))
            continue
        if block_type == BlockType.CODE:
            nodes.append(code_block_to_leafnode(block))
            continue
        if block_type == BlockType.QUOTE:
            nodes.append(quote_block_to_leafnode(block))
            continue
        if block_type == BlockType.UNORDERED_LIST:
            nodes.append(unorlist_block_to_HTMLNode(block))
            continue
        if block_type == BlockType.ORDERED_LIST:
            nodes.append(ordlist_block_to_HTMLNode(block))
            continue
        if block_type == BlockType.PARAGRAPH:
            nodes.append(paragraph_block_to_HTMLNode(block))
            continue
        raise ValueError("Unsuported Block type")
    return HTMLNode("div", children=nodes)
    
    # go trhoug all blocks to convert major blocks to their correscpoinding leaf nodde
    # except list have a list shell and list items as leafs
    # also paragraph has to chewed thoug inline checks to get it properly converted
