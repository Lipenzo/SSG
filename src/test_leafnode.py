import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        answer = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), answer)

    def test_eq2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        answer = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), answer)

if __name__ == "__main__":
    unittest.main()