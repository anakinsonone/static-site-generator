import os
import shutil
import sys

from generate_page import generate_pages_recursive


def copy_static_to_public() -> None:
    if not os.path.exists("static"):
        return
    if os.path.exists("docs"):
        shutil.rmtree("docs")

    def _copy_dir(src: str, dst: str) -> None:
        os.mkdir(dst)
        for entry in os.listdir(src):
            src_path = os.path.join(src, entry)
            dst_path = os.path.join(dst, entry)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copying {src_path} to {dst_path}")
            else:
                _copy_dir(src_path, dst_path)

    _copy_dir("static", "docs")


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
