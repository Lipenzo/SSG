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
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_split_list = node.text.split(delimiter)
        if len(text_split_list) % 2 == 0:
            raise SyntaxError(f"closing delmiter {delimiter} does not exist")
        for i in range(0, len(text_split_list)):
            if i % 2 == 0:
                if text_split_list[i] != "":
                    new_nodes.append(TextNode(text_split_list[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(text_split_list[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_pattern(old_nodes, pattern, text_type):
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
            new_nodes.append(TextNode(sections[i], text_type, sections[i +1]))
            if sections[i + 2] != "":
                new_nodes.append(TextNode(sections[i + 2], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return split_nodes_pattern(old_nodes, pattern, TextType.IMAGE)

def split_nodes_link(old_nodes):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return split_nodes_pattern(old_nodes, pattern, TextType.LINK)

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
