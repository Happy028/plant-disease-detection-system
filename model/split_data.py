import os
import shutil
import random

source_dir = "../dataset/train"
valid_dir = "../dataset/valid"

os.makedirs(valid_dir, exist_ok=True)

for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)
    
    if os.path.isdir(folder_path):
        images = os.listdir(folder_path)
        random.shuffle(images)

        split_size = int(len(images) * 0.1)  # 10% for validation

        valid_folder = os.path.join(valid_dir, folder)
        os.makedirs(valid_folder, exist_ok=True)

        for img in images[:split_size]:
            src = os.path.join(folder_path, img)
            dst = os.path.join(valid_folder, img)
            shutil.move(src, dst)

print("✅ Data split completed")