import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a",props={"href":"boot.dev"})
        output = node.props_to_html()
        output2 = ' href="boot.dev"'
        self.assertEqual(output, output2)

    def test_eq2(self):
        node = HTMLNode("h1","some text", props={"description":"des","href":"link.com"})
        output1 = node.props_to_html()
        output2 = ' description="des" href="link.com"'
        self.assertEqual(output1, output2)

    def test_eq3(self):
        node = HTMLNode("h2", props={"bb":"b","aa":"a"})
        node2 = HTMLNode("h1","has some text", props={"bb":"b","aa":"a"})
        output1 = node.props_to_html()
        output2 = node2.props_to_html()
        self.assertEqual(output1, output2)

if __name__ == "__main__":
    unittest.main()