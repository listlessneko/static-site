import os
from markdown_blocks import(
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    blocktype = block_to_block_type(blocks[0])
    
    if blocktype is BlockType.HEADING and blocks[0].startswith("# "):
        return blocks[0][2:]
    else:
        raise Exception("Must be heading 1")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'.")

    with open(from_path, "r") as f:
        md_contents = f.read()

    with open(template_path, "r") as f:
        template_contents = f.read()

    html_node = markdown_to_html_node(md_contents)
    html_string = html_node.to_html()
    title = extract_title(md_contents)

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)

