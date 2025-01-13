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

