class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):   
        if len(self.props) == 0:
            return "None"
        props = ""
        for prop in self.props:          
            props += f" {prop}:{self.props[prop]}"
        return props
    
    def __repr__(self):
        repr_string = "HTMLNode(\n"
        repr_string += f"    tag: {self.tag}\n"
        repr_string += f"    value: {self.value}\n"
        repr_string += "    children:"
        if len(self.children) == 0:
            repr_string += " None"
        for children in self.children:
            repr_string += f" {children.tag}"
        repr_string += "    props:"
        repr_string += self.props_to_html()
        repr_string += ")"