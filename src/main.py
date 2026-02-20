import os
from os.path import isfile
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode

PUBLIC_PATH = "public"
STATIC_PATH = "static"

def refresh_public(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def copy_static_to_public(src, dst):
    if os.path.exists(src):
        dirs = os.listdir(src)
        for dir in dirs:
            dir_path = os.path.join(src, dir)
            if os.path.isfile(dir_path):
                new_copy = shutil.copy(dir_path, dst)
                print(f"new copy -> {new_copy}")
            else:
                new_dir = os.path.join(dst, dir)
                os.mkdir(new_dir)
                copy_static_to_public(dir_path, new_dir)

def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown[1:]
    else:
        raise Exception("Must be heading 1")

def main():
    textnode = TextNode('This is some anchor text.', TextType.LINK, 'https://www.boot.dev')
    print(textnode)

    htmlnode = HTMLNode('test tag', 'test value', ['children'], {"href": "https://www.boot.dev", "target": "_blank"})
    print(htmlnode)

    refresh_public(PUBLIC_PATH)
    copy_static_to_public(STATIC_PATH, PUBLIC_PATH)

main()
