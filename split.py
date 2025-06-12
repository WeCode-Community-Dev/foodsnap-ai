import os
import shutil ,random

data_path = 'dataset/'

print("Looking in folder:", data_path)
print("Files in folder:", os.listdir(data_path))


train_folder = os.path.join("train_test/train")
test_folder = os.path.join("train_test/test")

image_extention = [".jpg",'.jpeg','.png']

img_list = []
for root,_,files in os.walk(data_path):
    for file in files:
        if os.path.splitext(file)[-1].lower() in image_extention:
            img_list.append(os.path.join(root,file))

print("Total images found:", len(img_list))
print("Sample file:", img_list[:5])

random.seed(40)

random.shuffle(img_list)

train_size = int(len(img_list)*0.80)
test_size = int(len(img_list)*0.20)

for folder_path in [train_folder,test_folder]:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 


for i , src_path in enumerate(img_list):
    if i < train_size:
        dest_folder = train_folder
    else:
        dest_folder = test_folder
    print(f"Copying {src_path} to {dest_folder}")
    filename = os.path.basename(src_path)
    shutil.copy(src_path,os.path.join(dest_folder,filename))