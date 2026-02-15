import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
            for index, part in enumerate(parts):
                if part == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text);
            if len(matches) == 0:
                new_nodes.append(old_node)
                continue

            remaining_text = old_node.text
            for i in range(len(matches)):
                current_match = matches[i]
                before, after = remaining_text.split(f"![{current_match[0]}]({current_match[1]})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(current_match[0], TextType.IMAGE, current_match[1]))
                remaining_text = after

            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text);
            if len(matches) == 0:
                new_nodes.append(old_node)
                continue

            remaining_text = old_node.text
            for i in range(len(matches)):
                current_match = matches[i]
                before, after = remaining_text.split(f"[{current_match[0]}]({current_match[1]})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(current_match[0], TextType.LINK, current_match[1]))
                remaining_text = after

            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
