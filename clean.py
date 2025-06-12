import os
from PIL import Image

def check_image(file_path):
    try:
        print("Cleaning...")
        with Image.open(file_path) as img:
            img.verify()
        return False
    except(IOError,SyntaxError) as e:
        print(f"Removing corrupted image: {file_path} - {e}")
        os.remove(file_path)
        return True

valid_exts = ['.jpg', '.jpeg', '.png']

def scan_image(directory):
    for root,dirs,files in os.walk(directory):
        for file in files:
            if not file.lower().endswith(tuple(valid_exts)):
                 print("Check validite")
                 os.remove(file)
            else:
                file_path = os.path.join(root,file)
                print("Image scan")
                check_image(file_path)
                
if __name__ == "__main__":
    # directory = "Users/josep/foodsnap/dataset"
    scan_image("foodsnap-ai/dataset")
    print("Directory scan and cleanup complete.")
