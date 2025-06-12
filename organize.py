import os
import shutil,re

def organize_images(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            cleaned = re.sub(r'\s*\([^)]*\)', '', filename)
            class_name = os.path.splitext(cleaned)[0]
            

            class_folder = os.path.join(folder_path, class_name)
            os.makedirs(class_folder, exist_ok=True)

            src_path = os.path.join(folder_path, filename)
            dst_path = os.path.join(class_folder, filename)
            shutil.move(src_path, dst_path)
            print(f"Moved {filename} → {class_name}/")

# Paths
train_folder = "train_test/train"
test_folder = "train_test/test"

# Run organization for both
organize_images(train_folder)
organize_images(test_folder)
