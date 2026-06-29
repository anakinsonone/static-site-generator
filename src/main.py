import os
import shutil

from generate_page import generate_pages_recursive


def copy_static_to_public() -> None:
    if not os.path.exists("static"):
        return
    if os.path.exists("public"):
        shutil.rmtree("public")
    shutil.copytree("static", "public")


def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
