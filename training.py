import os
import numpy as np
from PIL import Image

# ----------- IntelDataset Class -----------
class IntelDataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.image_files = []
        self.labels = []

        self.class_names = sorted(os.listdir(data_path))  # get class folder names
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.class_names)}
        print("Interldatset..")
        for cls in self.class_names:
            cls_folder = os.path.join(data_path, cls)
            for filename in os.listdir(cls_folder):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    self.image_files.append(os.path.join(cls_folder, filename))
                    self.labels.append(self.class_to_idx[cls])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        label = self.labels[idx]

        image = Image.open(img_path).convert("RGB")
        image = image.resize((224, 224))  # Resize all images to 224x224
        image = np.array(image) / 255.0   # Normalize to [0,1]
        return image, label

# ----------- Custom Dataloader -----------
class Dataloader:
    def __init__(self, dataset1, dataset2, batch_size, shuffle=False):
        print("dataloader ...")
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __len__(self):
        return min(len(self.dataset1), len(self.dataset2)) // self.batch_size

    def __iter__(self):
        data_len = self.__len__() * self.batch_size

        if self.shuffle:
            indices = np.random.permutation(data_len)
        else:
            indices = np.arange(data_len)

        for i in range(self.__len__()):
            batch_indices = indices[i * self.batch_size: (i + 1) * self.batch_size]

            batch1 = [self.dataset1[idx] for idx in batch_indices]
            images1, targets1 = zip(*batch1)
            images1 = np.stack(images1, axis=0)
            targets1 = np.stack(targets1, axis=0)

            batch2 = [self.dataset2[idx] for idx in batch_indices]
            images2, targets2 = zip(*batch2)
            images2 = np.stack(images2, axis=0)
            targets2 = np.stack(targets2, axis=0)

            yield images1, targets1, images2, targets2

# ----------- Initialize Datasets & Dataloader -----------
dataset1 = IntelDataset(data_path="train_test/train")
dataset2 = IntelDataset(data_path="train_test/test")

dataloader = Dataloader(dataset1, dataset2, batch_size=32, shuffle=False)

# ----------- Iterate Through Batches -----------
for i, (images1, targets1, images2, targets2) in enumerate(dataloader):
    print(f"Batch {i+1}")
    print("Train batch - images:", images1.shape, "labels:", targets1)
    print("Test batch  - images:", images2.shape, "labels:", targets2)
    
    if i == 2:  # Only show first 3 batches
        break
