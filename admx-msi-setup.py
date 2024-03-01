import os
import shutil
import tempfile
import urllib.request
import zipfile

TEMPDIR = tempfile.mkdtemp(dir="/tmp")
DESTDIR = "/usr/share/PolicyDefinitions/"

SOURCE_URL = "https://download.microsoft.com/download/3/0/6/30680643-987a-450c-b906-a455fff4aee8/Administrative%20Templates%20(.admx)%20for%20Windows%2010%20October%202020%20Update.msi"

def cleanup():
    print("Removing admx-msi-setup temporary files...")
    shutil.rmtree(TEMPDIR)

def download_files():
    urllib.request.urlretrieve(SOURCE_URL, f"{TEMPDIR}/package.msi")

def find_folder(root, target):
    for dirpath, dirnames, filenames in os.walk(root):
        if target in dirnames:
            return os.path.join(dirpath, target)
    return None

def extract_files():
    with zipfile.ZipFile(f"{TEMPDIR}/package.msi", 'r') as zip_ref:
        zip_ref.extractall(TEMPDIR)

    SOURCEDIR = find_folder(TEMPDIR, 'PolicyDefinitions')
    if not os.path.exists(SOURCEDIR):
        print("Policy definitions not found in package!")
        exit(1)
    else:
        if not os.path.exists(DESTDIR):
            os.makedirs(DESTDIR)
        for file in os.listdir(SOURCEDIR):
            shutil.copy(os.path.join(SOURCEDIR, file), DESTDIR)

def main():
    try:
        download_files()
        extract_files()
    finally:
        cleanup()

if __name__ == "__main__":
    main()

