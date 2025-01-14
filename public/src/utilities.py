from leafnode import LeafNode
from textnode import TextNode, TextType
import re

def text_to_node_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("unsupported text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        start = 0
        unfinished = True
        while unfinished:
            index = node.text.find(delimiter, start)
            if index == -1:
                new_nodes.append(TextNode(node.text[start:], node.text_type))
                unfinished = False
            elif index == start:
                index2 = node.text.find(delimiter, start + 1)
                if index2 == -1:
                    raise SyntaxError
                new_nodes.append(TextNode(node.text[start + 1: index2], text_type))
                start = index2 + 1
                if start == len(node.text):
                    unfinished = False
            else:
                new_nodes.append(TextNode(node.text[start:index], node.text_type))
                start = index
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_pattern(old_nodes, pattern, textnode_expr):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = re.split(pattern, node.text)
        if (len(sections) - 1) % 3 != 0:
            raise ValueError("Given text is unproperly formmated")
        if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        for i in range(1, len(sections), 3):
            new_nodes.append(textnode_expr(sections[i], sections[i + 1]))
            if sections[i + 2] != "":
                new_nodes.append(TextNode(sections[i + 2], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    expr = lambda a, b: TextNode("", TextType.IMAGE, {"alt":a, "src":b})
    return split_nodes_pattern(old_nodes, pattern, expr)

def split_nodes_link(old_nodes):
    pattern = r"\[(.*?)\]\((.*?)\)"
    expr = lambda a, b: TextNode(a, TextType.LINK, {"href":b})
    return split_nodes_pattern(old_nodes, pattern, expr)