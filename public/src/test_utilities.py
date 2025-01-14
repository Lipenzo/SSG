import unittest

from utilities import text_to_node_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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
        node3_output1 = TextNode("", TextType.IMAGE, {"alt":"text", "src":"image url"})
        node3_output2 = TextNode(" some more text", TextType.TEXT)
        nodes = [node, node2, node3]
        nodes_expected = [node, node2] + [node3_output1, node3_output2]
        return_nodes = split_nodes_image(nodes)
        self.assertEqual(str(nodes_expected), str(return_nodes))

    def test_split_node_image_onlyimg(self):
        node3 = TextNode("![text](image url)", TextType.TEXT)
        node3_output1 = TextNode("", TextType.IMAGE, {"alt":"text", "src":"image url"})
        nodes = [node3]
        nodes_expected = [node3_output1]
        return_nodes = split_nodes_image(nodes)
        self.assertEqual(str(nodes_expected), str(return_nodes))

    def test_split_node_link_doingsplit(self):
        node = TextNode("some text", TextType.TEXT)
        node2 = TextNode("another text", TextType.TEXT)
        node3 = TextNode("[text](image url) some more text", TextType.TEXT)
        node3_output1 = TextNode("text", TextType.LINK, {"href":"image url"})
        node3_output2 = TextNode(" some more text", TextType.TEXT)
        nodes = [node, node2, node3]
        nodes_expected = [node, node2] + [node3_output1, node3_output2]
        return_nodes = split_nodes_link(nodes)
        self.assertEqual(str(nodes_expected), str(return_nodes))

if __name__ == "__main__":
    unittest.main()