import os
import shutil
from copystatic import (
        copy_files_recursively
)
from gencontent import (
        generate_pages_recursively
)
from markdown_blocks import (
        BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node
)
from textnode import (
        TextNode,
        TextType
)
from htmlnode import (
        HTMLNode
)

PUBLIC_PATH = "./public/"
STATIC_PATH = "./static/"
CONTENT_PATH = "./content/"
TEMPLATE_PATH = "template.html"
PUBLIC_INDEX_HTML_PATH = "./public/index.html"

def main():
    textnode = TextNode('This is some anchor text.', TextType.LINK, 'https://www.boot.dev')
    print(textnode)

    htmlnode = HTMLNode('test tag', 'test value', ['children'], {"href": "https://www.boot.dev", "target": "_blank"})
    print(htmlnode)

    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)
    os.mkdir(PUBLIC_PATH)

    copy_files_recursively(STATIC_PATH, PUBLIC_PATH)
    generate_pages_recursively(CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH)

main()
