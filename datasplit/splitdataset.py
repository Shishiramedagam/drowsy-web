import os
import shutil
import random
from pathlib import Path

def create_split_dataset(src_dir, dest_dir, categories, split_ratio=0.8):
    for cat in categories:
        src_cat = Path(src_dir, cat)
        images = list(src_cat.glob("*"))
        random.shuffle(images)

        split_idx = int(len(images) * split_ratio)

        train_cat = Path(dest_dir, "train", cat)
        val_cat = Path(dest_dir, "val", cat)
        train_cat.mkdir(parents=True, exist_ok=True)
        val_cat.mkdir(parents=True, exist_ok=True)

        for img in images[:split_idx]:
            shutil.copy(img, train_cat)
        for img in images[split_idx:]:
            shutil.copy(img, val_cat)

# Split Eye Dataset
eye_src = r"C:\Users\dell\Downloads\drowsiness_data\eye_dataset"
eye_dest = r"C:\Users\dell\Downloads\drowsiness_data\processed_eyes"
create_split_dataset(eye_src, eye_dest, categories=["open", "closed"])

# Split Yawn Dataset
yawn_src = r"C:\Users\dell\Downloads\drowsiness_data\yawn_dataset"
yawn_dest = r"C:\Users\dell\Downloads\drowsiness_data\processed_yawn"
create_split_dataset(yawn_src, yawn_dest, categories=["yawn", "no_yawn"])

print("Datasets have been split into train and val sets!")
