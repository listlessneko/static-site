import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_bold(self):
        old_nodes = [
            TextNode("This is a text test.", TextType.TEXT),
            TextNode("This is a **bold** test.", TextType.TEXT),
            TextNode("This is **more bold** test.", TextType.TEXT),
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

        self.assertEqual(new_nodes[0].text, "This is a text test.")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "This is a ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, " test.")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "This is ")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "more bold")
        self.assertEqual(new_nodes[5].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[6].text, " test.")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)

    def test_split_nodes_with_not_text(self):
        old_nodes = [
            TextNode("`this is coding`", TextType.CODE),
            TextNode("this is *not* coding", TextType.TEXT),
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
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "not")
        self.assertEqual(new_nodes[2].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text, " coding")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)

    def test_split_unmatched_delimiter(self):
        old_node = TextNode("A **broken markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([old_node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_with_spacing(self):
        matches = extract_markdown_images("This is text with a    ![rick roll](https://i.imgur.com/aKaOqIh.gif)    and    ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)   ")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_no_matches(self):
        matches = extract_markdown_images("These are not the images you're looking for.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("This is text with ![](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_ignore_links(self):
        matches = extract_markdown_images("This is text with an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_with_spacing(self):
        matches = extract_markdown_links("This is text with a link     [to boot dev](https://www.boot.dev)    and     [to youtube](https://www.youtube.com/@bootdotdev)   ")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_no_matches(self):
        matches = extract_markdown_links("These are not the links you're looking for.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links("This is text with a link [](https://www.boot.dev)")
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_ignore_images(self):
        matches = extract_markdown_links("This is text with an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_split_nodes_image(self):
        node = TextNode("This is an image of ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), a jedi.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an image of ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", a jedi.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_image_no_text(self):
        node = TextNode("There is no text ![](https://i.imgur.com/fJRm4Vk.jpeg) here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There is no text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" here.", TextType.TEXT),
            ],
            new_nodes
        )


    def test_split_nodes_image_no_image(self):
        node = TextNode("There is no image here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There is no image here.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_image_start(self):
        node = TextNode("![Obi wan](https://i.imgur.com/fJRm4Vk.jpeg), a jedi.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", a jedi.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_image_end(self):
        node = TextNode("A jedi named ![Obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A jedi named ", TextType.TEXT),
                TextNode("Obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            new_nodes
        )

    def test_split_nodes_image_multiple(self):
        node = TextNode("There are two of them! Master ![Obi-Wan Kenobi](https://i.imgur.com/fJRm4Vk.jpeg) and ![Anakin Skywalker](https://i.imgur.com/fJRm4Vk.jpeg), his jedi apprentice.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There are two of them! Master ", TextType.TEXT),
                TextNode("Obi-Wan Kenobi", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Anakin Skywalker", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", his jedi apprentice.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("There are two of them! Master ![Obi-Wan Kenobi](https://i.imgur.com/fJRm4Vk.jpeg) and... ", TextType.TEXT),
            TextNode("![Anakin Skywalker](https://i.imgur.com/fJRm4Vk.jpeg), his jedi apprentice.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("There are two of them! Master ", TextType.TEXT),
                TextNode("Obi-Wan Kenobi", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and... ", TextType.TEXT),
                TextNode("Anakin Skywalker", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", his jedi apprentice.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_links(self):
        node = TextNode("Go to [boot dev](https://www.boot.dev) to become an archmage.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" to become an archmage.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_links_no_links(self):
        node = TextNode("There is no link here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("There is no link here.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_links_no_text(self):
        node = TextNode("Go to [](https://www.boot.dev) to become an archmage.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://www.boot.dev"),
                TextNode(" to become an archmage.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_links_start(self):
        node = TextNode("[Boot Dev](https://www.boot.dev), the place to become an archmage.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(", the place to become an archmage.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_links_end(self):
        node = TextNode("Become an archmage at [Boot Dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Become an archmage at ", TextType.TEXT),
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )

    def test_split_nodes_links_multiple(self):
        node = TextNode("Go to [Boot Dev](https://www.boot.dev) to become an archmage or go to [Steam](https://www.steam.com) to play video games.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" to become an archmage or go to ", TextType.TEXT),
                TextNode("Steam", TextType.LINK, "https://www.steam.com"),
                TextNode(" to play video games.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_nodes_links_multiple_nodes(self):
        nodes = [
            TextNode("Go to [Boot Dev](https://www.boot.dev) to become an archmage or...", TextType.TEXT),
            TextNode("go to [Steam](https://www.steam.com) to play video games.", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" to become an archmage or...", TextType.TEXT),
                TextNode("go to ", TextType.TEXT),
                TextNode("Steam", TextType.LINK, "https://www.steam.com"),
                TextNode(" to play video games.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "If **you** want to learn the _ancient arts_ and write `arcane, codified systems`, then travel through the ![portal](https://i.imgur.com/fJRm4Vk.jpeg) and go to [Boot Dev](https://www.boot.dev)."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("If ", TextType.TEXT),
                TextNode("you", TextType.BOLD),
                TextNode(" want to learn the ", TextType.TEXT),
                TextNode("ancient arts", TextType.ITALIC),
                TextNode(" and write ", TextType.TEXT),
                TextNode("arcane, codified systems", TextType.CODE),
                TextNode(", then travel through the ", TextType.TEXT),
                TextNode("portal", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(".", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_unordered(self):
        text = "Go to [Boot Dev](https://www.boot.dev) by traveling through the ![portal](https://i.imgur.com/fJRm4Vk.jpeg), to _learn_ the **ancient arts** and write `arcane, codified systems`."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" by traveling through the ", TextType.TEXT),
                TextNode("portal", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", to ", TextType.TEXT),
                TextNode("learn", TextType.ITALIC),
                TextNode(" the ", TextType.TEXT),
                TextNode("ancient arts", TextType.BOLD),
                TextNode(" and write ", TextType.TEXT),
                TextNode("arcane, codified systems", TextType.CODE),
                TextNode(".", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_only_text(self):
        text = "If you want to learn the ancient arts and write arcane, codified systems, then travel through the portal and go to Boot Dev."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("If you want to learn the ancient arts and write arcane, codified systems, then travel through the portal and go to Boot Dev.", TextType.TEXT),
            ],
            nodes
        )

    def test_text_to_textnodes_multiple_of_same(self):
        text = "If _you_ want to learn the _ancient arts_ and write _arcane, codified systems_, then travel through the _portal_ and go to _Boot Dev_."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("If ", TextType.TEXT),
                TextNode("you", TextType.ITALIC),
                TextNode(" want to learn the ", TextType.TEXT),
                TextNode("ancient arts", TextType.ITALIC),
                TextNode(" and write ", TextType.TEXT),
                TextNode("arcane, codified systems", TextType.ITALIC),
                TextNode(", then travel through the ", TextType.TEXT),
                TextNode("portal", TextType.ITALIC),
                TextNode(" and go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            nodes
        )

    def test_text_to_textnodes_multiple_of_multiple_same(self):
        text = "If **you** want to learn the _ancient arts_ and write _arcane, codified systems_, then travel through the **portal** and go to _Boot Dev_."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("If ", TextType.TEXT),
                TextNode("you", TextType.BOLD),
                TextNode(" want to learn the ", TextType.TEXT),
                TextNode("ancient arts", TextType.ITALIC),
                TextNode(" and write ", TextType.TEXT),
                TextNode("arcane, codified systems", TextType.ITALIC),
                TextNode(", then travel through the ", TextType.TEXT),
                TextNode("portal", TextType.BOLD),
                TextNode(" and go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            nodes
        )

    def test_text_to_textnodes_delimiters_inside_delimiters(self):
        text = "If **you** want to learn the _`ancient arts`_ and write _`arcane, codified systems`_, then travel through the **portal** and go to _Boot Dev_."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("If ", TextType.TEXT),
                TextNode("you", TextType.BOLD),
                TextNode(" want to learn the ", TextType.TEXT),
                TextNode("`ancient arts`", TextType.ITALIC),
                TextNode(" and write ", TextType.TEXT),
                TextNode("`arcane, codified systems`", TextType.ITALIC),
                TextNode(", then travel through the ", TextType.TEXT),
                TextNode("portal", TextType.BOLD),
                TextNode(" and go to ", TextType.TEXT),
                TextNode("Boot Dev", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            nodes
        )

    def test_text_to_textnodes_delimiters_inside_delimiters_again(self):
        text = "If **you** want to learn the `_ancient arts_` and write `_arcane, codified systems_`, then travel through the **portal** and go to _Boot Dev_."
        with self.assertRaises(Exception):
            nodes = text_to_textnodes(text)

if __name__ == "__main__":
    unittest.main()
