from utilities import extract_title
from os.path import dirname, join, isfile
from os import makedirs, listdir
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

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for file in listdir(dir_path_content):
        file_path = join(dir_path_content, file)
        dest_path = join(dest_dir_path, file)
        new_file_name = "".join(file.split(".")[:-1])+".html"
        New_file_path = join(dest_dir_path, new_file_name)
        if isfile(file_path):
            generate_page(file_path, template_path, New_file_path)
        else:
            generate_pages_recursively(file_path, template_path, dest_path)