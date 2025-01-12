import unittest

from utilities import text_to_node_html_node, split__nodes_delimeter
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
        output = split__nodes_delimeter(input_list, "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))
    
    def test_split_delim_in_midle(self):
        text_node = TextNode("some 'code inside' text", TextType.TEXT)
        answer_node1 = TextNode("some ", TextType.TEXT)
        answer_node2 = TextNode("code inside", TextType.CODE)
        answer_node3 = TextNode(" text", TextType.TEXT)
        input_list = [answer_node1, answer_node2, answer_node3]
        output = split__nodes_delimeter([text_node], "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))

    def test_split_delim_in_front(self):
        text_node = TextNode("'some code inside' text", TextType.TEXT)
        answer_node2 = TextNode("some code inside", TextType.CODE)
        answer_node3 = TextNode(" text", TextType.TEXT)
        input_list = [answer_node2, answer_node3]
        output = split__nodes_delimeter([text_node], "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))

    def test_split_delim_in_end(self):
        text_node = TextNode("some code inside 'text'", TextType.TEXT)
        answer_node2 = TextNode("some code inside ", TextType.TEXT)
        answer_node3 = TextNode("text", TextType.CODE)
        input_list = [answer_node2, answer_node3]
        output = split__nodes_delimeter([text_node], "'", TextType.CODE) 
        self.assertEqual(str(output), str(input_list))

    def test_multi_split(self):
        text_node1 = TextNode("some code inside 'text'", TextType.TEXT)
        text_node2 = TextNode("litle *fox* jumped over mule", TextType.TEXT)
        input_list = [text_node1, text_node2]
        answer_node2 = TextNode("some code inside ", TextType.TEXT)
        answer_node3 = TextNode("text", TextType.CODE)
        answer_list = [answer_node2, answer_node3,text_node2]
        output_list = split__nodes_delimeter(input_list, "'", TextType.CODE) 
        self.assertEqual(str(answer_list), str(output_list))

    def test_split_sintax_err(self):
        text_node1 = TextNode("some code inside text'", TextType.TEXT)
        text_node2 = TextNode("litle *fox* jumped over mule", TextType.TEXT)
        input_list = [text_node1, text_node2]
        with self.assertRaises(SyntaxError):
            output_list = split__nodes_delimeter(input_list, "'", TextType.CODE) 

if __name__ == "__main__":
    unittest.main()