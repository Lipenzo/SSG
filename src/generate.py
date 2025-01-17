from utilities import extract_title
from os.path import dirname
from os import makedirs
from markdowtohtmlnode import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    # ensuring directories leading to file exist
    makedirs(dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)