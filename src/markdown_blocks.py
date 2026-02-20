from enum import Enum

from htmlnode import (
        LeafNode,
        ParentNode
)
from inline_markdown import (
        text_to_textnodes
)
from textnode import (
        text_node_to_html_node
)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    counter = 0
    for line in lines:
        counter += 1
        if not line.startswith(f"{counter}."):
            counter = 0
            break
    if counter == len(lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    return [s.strip() for s in markdown.split('\n\n') if s.strip()]

def text_to_children_html_nodes(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = list(map(lambda text_node: text_node_to_html_node(text_node), text_nodes))
    return children_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype is BlockType.HEADING:
            heading_text = block.lstrip('#')
            tag = f"h{str(len(block) - len(heading_text))}"
            children_nodes = text_to_children_html_nodes(heading_text[1:])
            new_node = ParentNode(tag, children_nodes)
            block_nodes.append(new_node)
        elif blocktype is BlockType.CODE:
            code_text = block.strip("```").lstrip("\n")
            code_node = LeafNode("code", code_text)
            pre_node = ParentNode("pre", [code_node])
            block_nodes.append(pre_node)
        elif blocktype is BlockType.QUOTE:
            lines = block.split("\n")
            quote_text = " ".join(line.lstrip("> ") for line in lines)
            children_nodes = text_to_children_html_nodes(quote_text)
            new_node = ParentNode("blockquote", children_nodes)
            block_nodes.append(new_node)
        elif blocktype is BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            ul_children_nodes = []
            for line in lines:
                children_nodes = text_to_children_html_nodes(line[2:])
                parent_node = ParentNode("li", children_nodes)
                ul_children_nodes.append(parent_node)
            ul_nodes = ParentNode("ul", ul_children_nodes)
            block_nodes.append(ul_nodes)
        elif blocktype is BlockType.ORDERED_LIST:
            lines = block.split("\n")
            ol_children_nodes = []
            for line in lines:
                children_nodes = text_to_children_html_nodes(line.split(". ", 1)[1])
                parent_node = ParentNode("li", children_nodes)
                ol_children_nodes.append(parent_node)
            ol_nodes = ParentNode("ol", ol_children_nodes)
            block_nodes.append(ol_nodes)
        else:
            lines = " ".join(block.split("\n"))
            children_nodes = text_to_children_html_nodes(lines)
            new_node = ParentNode("p", children_nodes)
            block_nodes.append(new_node)
    div_node = ParentNode("div", block_nodes)
    return div_node
