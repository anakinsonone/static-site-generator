import os
import pathlib

from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dir_path_public: str, basepath: str) -> None:
    for root, _dirs, files in os.walk(dir_path_content):
        for file in files:
            if not file.endswith(".md"):
                continue
            from_path = os.path.join(root, file)
            rel_path = os.path.relpath(from_path, dir_path_content)
            dest_path = os.path.join(dir_path_public, rel_path.replace(".md", ".html"))
            generate_page(from_path, template_path, dest_path, basepath)
