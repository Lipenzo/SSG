import unittest

from block import BlockType, block_to_html_type

class TestBlock(unittest.TestCase):
    def test_block_to_block_type1(self):
        input_block = "##### some text"
        expected_block_type = BlockType.HEADING
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type2(self):
        input_block = "############### some text"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type3(self):
        input_block = "####### some text\n"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type4(self):
        input_block = "###### some text\n"
        expected_block_type = BlockType.HEADING
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)
    
    def test_block_to_block_type5(self):
        input_block = "```some text\n```"
        expected_block_type = BlockType.CODE
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type6(self):
        input_block = "```some text\n``` "
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type7(self):
        input_block = " ```some text\n```"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type8(self):
        input_block = "> Quote"
        expected_block_type = BlockType.QUOTE
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type9(self):
        input_block = ">still quote"
        expected_block_type = BlockType.QUOTE
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type10(self):
        input_block = "> quote line\nbraking quote"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type11(self):
        input_block = "* unordered list item"
        expected_block_type = BlockType.UNORDERED_LIST
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type12(self):
        input_block = "* unordered list item\n- another unordered list line"
        expected_block_type = BlockType.UNORDERED_LIST
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type13(self):
        input_block = "*no spacing mean a paragraph"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type14(self):
        input_block = "* this line OK\n*But this not"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type15(self):
        input_block = "1. One item in a ordered list"
        expected_block_type = BlockType.ORDERED_LIST
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type16(self):
        input_block = "1. One item in a ordered list\n2. second itme in a list\n3. third item"
        expected_block_type = BlockType.ORDERED_LIST
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

    def test_block_to_block_type17(self):
        input_block = "1. One item in a ordered list\n3. skipped number should make it into a normal paragraph"
        expected_block_type = BlockType.PARAGRAPH
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)
    
    def test_block_to_block_type18(self):
        input_block = " 1. space in start should break it into normal paragraph too"
        expected_block_type = BlockType.ORDERED_LIST
        output_block_type = block_to_html_type(input_block)
        self.assertEqual(expected_block_type, output_block_type)

if __name__ == "__main__":
    unittest.main()