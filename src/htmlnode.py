class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            formatted_string = ''
            for k, v in self.props.items():
                formatted_string += f' {k}="{v}"'
            return formatted_string
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('node must have a value')
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if self.tag is None:
            raise ValueError('node must have a tag')
        if self.children is None:
            raise ValueError('children must have value')

        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()

        props_html = ""
        if self.props:
            props_html += self.props_to_html()

        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

