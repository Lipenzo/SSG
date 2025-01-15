import unittest

from utilities import text_to_node_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes, markdown_to_blocks
from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node = TextNode("some Text", TextType.TEXT)
        leaf = LeafNode(None, "some Text")
        converted = text_to_node_html_node(text_node)
        self.assertEqual(leaf.to_html(), converted.to_html())

    def test_eq2(self):
        text_node = TextNode("some Text", TextType.BOLD)
        leaf = LeafNode("b", "some Text")
        converted = text_to_node_html_node(text_node)
        self.assertEqual(leaf.to_html(), converted.to_html())

    def test_eq3(self):
        text_node = TextNode("some Text", TextType.ITALIC)
        leaf = LeafNode("i", "some Text")
        converted = text_to_node_html_node(text_node)
        self.assertEqual(leaf.to_html(), converted.to_html())

    def test_eq4(self):
        text_node = TextNode("some Text", TextType.CODE)
        leaf = LeafNode("code", "some Text")
        converted = text_to_node_html_node(text_node)
        self.assertEqual(leaf.to_html(), converted.to_html())

    def test_eq5(self):
        text_node = TextNode("some Text", TextType.LINK, "link")
        leaf = LeafNode("a", "some Text",{"href":"link"})
        converted = text_to_node_html_node(text_node)
        self.assertEqual(leaf.to_html(), converted.to_html())

    def test_eq6(self):
        text_node = TextNode("some Text", TextType.IMAGE, "link")
        leaf = LeafNode("img", "",{"src":"link", "alt":"some Text"})
        converted = text_to_node_html_node(text_node)
        self.assertEqual(leaf.to_html(), converted.to_html())

# split modes delimiter tests

    def test_split_no_delim_in_text(self):
        text_node = TextNode("some text", TextType.TEXT)
        input_list = [text_node]
        output = split_nodes_delimiter(input_list, "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))
    
    def test_split_delim_in_midle(self):
        text_node = TextNode("some 'code inside' text", TextType.TEXT)
        answer_node1 = TextNode("some ", TextType.TEXT)
        answer_node2 = TextNode("code inside", TextType.CODE)
        answer_node3 = TextNode(" text", TextType.TEXT)
        input_list = [answer_node1, answer_node2, answer_node3]
        output = split_nodes_delimiter([text_node], "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))

    def test_split_delim_in_front(self):
        text_node = TextNode("'some code inside' text", TextType.TEXT)
        answer_node2 = TextNode("some code inside", TextType.CODE)
        answer_node3 = TextNode(" text", TextType.TEXT)
        input_list = [answer_node2, answer_node3]
        output = split_nodes_delimiter([text_node], "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))

    def test_split_delim_in_end(self):
        text_node = TextNode("some code inside 'text'", TextType.TEXT)
        answer_node2 = TextNode("some code inside ", TextType.TEXT)
        answer_node3 = TextNode("text", TextType.CODE)
        input_list = [answer_node2, answer_node3]
        output = split_nodes_delimiter([text_node], "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))
    
    def test_split_delim_bold(self):
        text_node = TextNode("This is **text** with an *italic* word and a ", TextType.TEXT)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an *italic* word and a ", TextType.TEXT)
        ]
        output_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(str(output_nodes), str(expected_nodes))

    def test_multi_split(self):
        text_node1 = TextNode("some code inside 'text'", TextType.TEXT)
        text_node2 = TextNode("litle *fox* jumped over mule", TextType.TEXT)
        input_list = [text_node1, text_node2]
        answer_node2 = TextNode("some code inside ", TextType.TEXT)
        answer_node3 = TextNode("text", TextType.CODE)
        answer_list = [answer_node2, answer_node3,text_node2]
        output_list = split_nodes_delimiter(input_list, "'", TextType.CODE) 
        self.assertEqual(str(answer_list), str(output_list))

    def test_split_sintax_err(self):
        text_node1 = TextNode("some code inside text'", TextType.TEXT)
        text_node2 = TextNode("litle *fox* jumped over mule", TextType.TEXT)
        input_list = [text_node1, text_node2]
        with self.assertRaises(SyntaxError):
            output_list = split_nodes_delimiter(input_list, "'", TextType.CODE) 

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        answer = extract_markdown_images(text)
        expected_answer = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(str(answer), str(expected_answer))

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        answer = extract_markdown_links(text)
        expected_answer = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(str(answer), str(expected_answer))

    def test_split_node_image_onlytext(self):
        node = TextNode("some text", TextType.TEXT)
        return_nodes = split_nodes_image([node])
        self.assertEqual(str([node]), str(return_nodes))
    
    def test_split_node_image_onlytextmulti(self):
        node = TextNode("some text", TextType.TEXT)
        node2 = TextNode("another text", TextType.TEXT)
        nodes = [node, node2]
        return_nodes = split_nodes_image(nodes)
        self.assertEqual(str(nodes), str(return_nodes))

    def test_split_node_image_onlytextmultitype(self):
        node = TextNode("some text", TextType.TEXT)
        node2 = TextNode("another text", TextType.TEXT)
        node3 = TextNode("![text](imgae url) some more text", TextType.CODE)
        nodes = [node, node2, node3]
        return_nodes = split_nodes_image(nodes)
        self.assertEqual(str(nodes), str(return_nodes))

    def test_split_node_image_doingsplit(self):
        node = TextNode("some text", TextType.TEXT)
        node2 = TextNode("another text", TextType.TEXT)
        node3 = TextNode("![text](image url) some more text", TextType.TEXT)
        node3_output1 = TextNode("text", TextType.IMAGE, "image url")
        node3_output2 = TextNode(" some more text", TextType.TEXT)
        nodes = [node, node2, node3]
        nodes_expected = [node, node2] + [node3_output1, node3_output2]
        return_nodes = split_nodes_image(nodes)
        self.assertEqual(str(nodes_expected), str(return_nodes))

    def test_split_node_image_onlyimg(self):
        node3 = TextNode("![text](image url)", TextType.TEXT)
        node3_output1 = TextNode("text", TextType.IMAGE, "image url")
        nodes = [node3]
        nodes_expected = [node3_output1]
        return_nodes = split_nodes_image(nodes)
        self.assertEqual(str(nodes_expected), str(return_nodes))

    def test_split_node_link_doingsplit(self):
        node = TextNode("some text", TextType.TEXT)
        node2 = TextNode("another text", TextType.TEXT)
        node3 = TextNode("[text](image url) some more text", TextType.TEXT)
        node3_output1 = TextNode("text", TextType.LINK, "image url")
        node3_output2 = TextNode(" some more text", TextType.TEXT)
        nodes = [node, node2, node3]
        nodes_expected = [node, node2] + [node3_output1, node3_output2]
        return_nodes = split_nodes_link(nodes)
        self.assertEqual(str(nodes_expected), str(return_nodes))

    def test_text_nodes_to_text_example(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        function_nodes = text_to_text_nodes(input_text)
        self.assertEqual(str(function_nodes), str(expected_nodes))

    def test_markdown_to_blocks1(self):
        imput_markdown =  "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        output_block1 = "# This is a heading"
        output_block2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        output_block3 = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        output_list = [output_block1, output_block2, output_block3]
        answer_block = markdown_to_blocks(imput_markdown)
        self.assertEqual(output_list, answer_block)

    def test_markdown_to_blocks1(self):
        imput_markdown =  "          \n\n            # This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n   \n\n\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        output_block1 = "# This is a heading"
        output_block2 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        output_block3 = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        output_list = [output_block1, output_block2, output_block3]
        answer_block = markdown_to_blocks(imput_markdown)
        self.assertEqual(output_list, answer_block)


if __name__ == "__main__":
    unittest.main()