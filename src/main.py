from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    textnode = TextNode('This is some anchor text.', TextType.LINK, 'https://www.boot.dev')
    print(textnode)

    htmlnode = HTMLNode('test tag', 'test value', ['children'], {"href": "https://www.boot.dev", "target": "_blank"})
    print(htmlnode)

main()
