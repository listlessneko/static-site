import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_bold(self):
        old_nodes = [
            TextNode("This is a plain test.", TextType.PLAIN),
            TextNode("This is a **bold** test.", TextType.PLAIN),
            TextNode("This is **more bold** test.", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 7)
        self.assertIsInstance(new_nodes[0], TextNode)
        self.assertIsInstance(new_nodes[1], TextNode)
        self.assertIsInstance(new_nodes[2], TextNode)
        self.assertIsInstance(new_nodes[3], TextNode)
        self.assertIsInstance(new_nodes[4], TextNode)
        self.assertIsInstance(new_nodes[5], TextNode)
        self.assertIsInstance(new_nodes[6], TextNode)

        self.assertEqual(new_nodes[0].text, "This is a plain test.")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text, "This is a ")
        self.assertEqual(new_nodes[1].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, " test.")
        self.assertEqual(new_nodes[3].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[4].text, "This is ")
        self.assertEqual(new_nodes[4].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[5].text, "more bold")
        self.assertEqual(new_nodes[5].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[6].text, " test.")
        self.assertEqual(new_nodes[6].text_type, TextType.PLAIN)

    def test_split_nodes_with_not_plain(self):
        old_nodes = [
            TextNode("`this is coding`", TextType.CODE),
            TextNode("this is *not* coding", TextType.PLAIN),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 4)
        self.assertIsInstance(new_nodes[0], TextNode)
        self.assertIsInstance(new_nodes[1], TextNode)
        self.assertIsInstance(new_nodes[2], TextNode)
        self.assertIsInstance(new_nodes[3], TextNode)

        self.assertEqual(new_nodes[0].text, "`this is coding`")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "this is ")
        self.assertEqual(new_nodes[1].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[2].text, "not")
        self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text, " coding")
        self.assertEqual(new_nodes[3].text_type, TextType.PLAIN)

    def test_split_unmatched_delimiter(self):
        old_node = TextNode("A **broken markdown", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([old_node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
