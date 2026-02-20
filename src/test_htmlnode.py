import unittest

from htmlnode import (
        HTMLNode,
        LeafNode,
        ParentNode
)

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_props_single(self):
        node = LeafNode("a", "Foo Bar", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Foo Bar</a>')

    def test_leaf_to_html_props_multiple(self):
        node = LeafNode("a", "Foo Bar", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Foo Bar</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just foo")
        self.assertEqual(node.to_html(), "Just foo")

    def test_leaf_to_html_empty_string(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_repr_(self):
        node = LeafNode("p", "foo", {"class": "greeting"})
        self.assertEqual(repr(node), "LeafNode(p, foo, {'class': 'greeting'})")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_parent_tag_none(self):
        child_node = LeafNode("p", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_missing_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.to_html(), "<p></p>")

    def test_to_html_mix_children(self):
        leaf_child = LeafNode(None, "leaf_child")
        child = ParentNode("span", [leaf_child, leaf_child, leaf_child])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>leaf_childleaf_childleaf_child</span></div>")

    def test_to_html_props_on_parent(self):
        leaf_child = LeafNode(None, "leaf_child")
        parent = ParentNode("div", [leaf_child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container">leaf_child</div>')

if __name__ == "__main__":
    unittest.main()
