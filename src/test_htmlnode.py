import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="foo",
            children=['foo', 'bar'],
            props={"href": "https://example.com"}
        )
        self.assertEqual(repr(node), f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})")

    def test_html_init_none1(self):
        node = HTMLNode(
            tag="a",
            value="foo"
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "foo")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_html_init_none2(self):
        node = HTMLNode(
            children=['foo', 'bar'],
        )
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, ['foo', 'bar'])
        self.assertEqual(node.props, None)

    def test_props_formatting_single(self):
        node = HTMLNode(
            tag="a",
            value="foo",
            props={"href": "https://example.com"}
        )
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_formatting_multiple(self):
        node = HTMLNode(
            tag="a",
            value="foo",
            props={"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')


    def test_props_formatting_none(self):
        node = HTMLNode(
            tag="a",
            value="foo",
            props=None
        )
        self.assertEqual(node.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()
