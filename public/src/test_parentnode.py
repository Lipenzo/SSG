import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ]
    )
        answer = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), answer)

    def test_err(self):
        node = ParentNode(None, ["b","bold text"])
        err = ValueError
        with self.assertRaises(err):
            node.to_html()

    def test_err2(self):
        node = ParentNode("h1", [])
        err = ValueError
        with self.assertRaises(err):
            node.to_html()

    def test_eq2(self):
        node = ParentNode("h1", 
                          [LeafNode("a","some link")],
                            {"href": "https://www.google.com"})
        err = ValueError
        answer = '<h1 href="https://www.google.com"><a>some link</a></h1>'
        self.assertCountEqual(node.to_html(), answer)

if __name__ == "__main__":
    unittest.main()