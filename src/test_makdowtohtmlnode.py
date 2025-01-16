import unittest
from markdowtohtmlnode import heading_block_to_leafnode, code_block_to_leafnode, quote_block_to_leafnode, unorlist_block_to_HTMLNode, ordlist_block_to_HTMLNode, markdown_to_html_node
from leafnode import LeafNode
from htmlnode import HTMLNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading_block_to_leafnode1(self):
        block = "## level 2 heading leaf node"
        expected_output = LeafNode("h2", "level 2 heading leaf node")
        output = heading_block_to_leafnode(block)
        self.assertEqual(str(expected_output), str(output))

    def test_code_block_to_leafnode(self):
        block = "```text code\n some moretext```"
        expected_output = LeafNode("code", "text code\n some moretext")
        output = code_block_to_leafnode(block)
        self.assertEqual(str(expected_output), str(output))

    def test_quote_block_to_leafnode(self):
        block = "> quotable text\n> another line of quotable text"
        expected_output = LeafNode("blockquote", "quotable text\nanother line of quotable text")
        output = quote_block_to_leafnode(block)
        self.assertEqual(str(expected_output), str(output))

    def test_unordlist_block_to_HTMLNode(self):
        block = "- first item\n- second item"
        iter_leaf = LeafNode("li", "first item")
        iter_leaf2 = LeafNode("li", "second item")
        expected_output = HTMLNode("ul", children=[iter_leaf, iter_leaf2])
        output = unorlist_block_to_HTMLNode(block)
        self.assertEqual(str(expected_output), str(output))
        
    def test_ordlist_block_to_HTMLNode(self):
        block = "1. first item\n2. second item"
        iter_leaf = LeafNode("li", "first item")
        iter_leaf2 = LeafNode("li", "second item")
        expected_output = HTMLNode("ol", children=[iter_leaf, iter_leaf2])
        output = ordlist_block_to_HTMLNode(block)
        self.assertEqual(str(expected_output), str(output))

    def test_ordlist_block_to_HTMLNode_above_ten(self):
        block = "1. first item\n2. second item\n3. 3\n4. 4\n5. 5\n6. 6\n7. 7\n8. 8\n9. 9\n10. 10"
        iter_leaf = LeafNode("li", "first item")
        iter_leaf2 = LeafNode("li", "second item")
        iter_leaf3 = LeafNode("li", "3")
        iter_leaf4 = LeafNode("li", "4")
        iter_leaf5 = LeafNode("li", "5")
        iter_leaf6 = LeafNode("li", "6")
        iter_leaf7 = LeafNode("li", "7")
        iter_leaf8 = LeafNode("li", "8")
        iter_leaf9 = LeafNode("li", "9")
        iter_leaf10 = LeafNode("li", "10")
        expected_output = HTMLNode("ol", children=[iter_leaf, iter_leaf2, iter_leaf3, iter_leaf4, iter_leaf5, iter_leaf6, iter_leaf7, iter_leaf8, iter_leaf9, iter_leaf10])
        output = ordlist_block_to_HTMLNode(block)
        self.assertEqual(str(expected_output), str(output))

    def test_markdown_to_html_node(self):
        markdown = "# Header\n\nParagraph\n\n- list item\n- list item\n\n[link](somewhere)\n\n![image](something)\n\n*italics*\n\n**bold**"
        header = LeafNode("h1", "Header")
        simple_paragraph = LeafNode(None, "Paragraph")
        list_item = LeafNode("li", "list item")
        unordered_list = HTMLNode("ul", children=[list_item, list_item])
        link = LeafNode("a", "link", props={"href":"somewhere"})
        image = LeafNode("img", None, props={"src":"image", "alt":"something"})
        italic_text = LeafNode("i", "italics")
        bold_text = LeafNode("b", "bold")
        expected_output = HTMLNode("div", children=[header, simple_paragraph,unordered_list, link, image, italic_text, bold_text])
        output = markdown_to_html_node(markdown)
        self.assertEqual(str(expected_output), str(output))

    def test_markdown_to_html_node2(self):
        markdown = "# Header\n\nParagraph\n\n- list item\n- list item\n\n[link](somewhere)\n\n![image](something)\n\n*italics* **bold**"
        header = LeafNode("h1", "Header")
        simple_paragraph = LeafNode(None, "Paragraph")
        list_item = LeafNode("li", "list item")
        unordered_list = HTMLNode("ul", children=[list_item, list_item])
        link = LeafNode("a", "link", props={"href":"somewhere"})
        image = LeafNode("img", None, props={"src":"image", "alt":"something"})
        italic_text = LeafNode("i", "italics")
        bold_text = LeafNode("b", "bold")
        space = LeafNode(None, " ")
        last_paragraph =HTMLNode("p", children=[italic_text, space, bold_text])
        expected_output = HTMLNode("div", children=[header, simple_paragraph,unordered_list, link, image, last_paragraph])
        output = markdown_to_html_node(markdown)
        self.assertEqual(str(expected_output), str(output))

    def test_markdown_to_html_node3(self):
        markdown = "# Header\n\nParagraph\n\n- list item\n- list item\n\n[link](somewhere)\n\n![image](something)\n\n**italics** **bold**"
        header = LeafNode("h1", "Header")
        simple_paragraph = LeafNode(None, "Paragraph")
        list_item = LeafNode("li", "list item")
        unordered_list = HTMLNode("ul", children=[list_item, list_item])
        link = LeafNode("a", "link", props={"href":"somewhere"})
        image = LeafNode("img", None, props={"src":"image", "alt":"something"})
        italic_text = LeafNode("i", "italics")
        bold_text = LeafNode("b", "bold")
        space = LeafNode(None, " ")
        last_paragraph =HTMLNode("p", children=[italic_text, space, bold_text])
        expected_output = HTMLNode("div", children=[header, simple_paragraph,unordered_list, link, image, last_paragraph])
        output = markdown_to_html_node(markdown)
        self.assertNotEqual(str(expected_output), str(output))

if __name__ == "__main__":
    unittest.main()