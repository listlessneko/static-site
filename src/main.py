import sys
import os
import shutil
from copystatic import (
        copy_files_recursively
)
from gencontent import (
        generate_pages_recursively
)

BASE_PATH = sys.argv[1]
DEST_PATH = "./docs/"
STATIC_PATH = "./static/"
CONTENT_PATH = "./content/"
TEMPLATE_PATH = "template.html"

def main():
    print(f"Refreshing {DEST_PATH}...")
    if os.path.exists(DEST_PATH):
        shutil.rmtree(DEST_PATH)
    os.mkdir(DEST_PATH)

    print(f"Copying static files to public directory...")
    copy_files_recursively(STATIC_PATH, DEST_PATH)
    generate_pages_recursively(CONTENT_PATH, TEMPLATE_PATH, DEST_PATH, BASE_PATH)

main()
