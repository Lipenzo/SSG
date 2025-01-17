class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.children == None:
            raise ValueError("Trying to generate html out of HTML node without any children")
        return f"<{self.tag}>{self.__form_html_string_from_children()}</{self.tag}>"
    
    def __form_html_string_from_children(self):
        final_string = ""
        for child in self.children:
            final_string += child.to_html()
        return final_string

    def props_to_html(self):   
        if self.props == None or len(self.props) == 0:
            return ""
        props = ""
        for prop in self.props:          
            props += f' {prop}="{self.props[prop]}"'
        return props
    
    def __children_list(self):
        repr = str(self.tag)
        if self.children != None:
            children = []
            for child in self.children:
                children.append(child.__children_list())
            repr += "[" + " ".join(children) + "]"
        return repr

    def __repr__(self):
        repr_string = "HTMLNode(\n"
        repr_string += f"    tag: {self.tag}\n"
        repr_string += f"    value: {self.value}\n"
        repr_string += "    children:"
        if self.children == None or len(self.children) == 0:
            repr_string += " None"
        else:
            for children in self.children:
                repr_string += f" {children.__children_list()}"
        repr_string += "    props:"
        repr_string += self.props_to_html()
        repr_string += ")"
        return repr_string