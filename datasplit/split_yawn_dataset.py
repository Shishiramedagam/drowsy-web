import os
import shutil
import random

source_dir = r"C:\Users\dell\Downloads\yawn_dataset"
output_dir = r"C:\Users\dell\Downloads\drowsiness_data\yawn_split"

train_ratio = 0.8  # 80% train, 20% val

# Correct folder names
yawn_dir = os.path.join(source_dir, "yawn")
no_yawn_dir = os.path.join(source_dir, "no yawn")  # <-- FIXED

# Output subfolders
train_yawn = os.path.join(output_dir, "train", "yawn")
train_no_yawn = os.path.join(output_dir, "train", "no_yawn")
val_yawn = os.path.join(output_dir, "val", "yawn")
val_no_yawn = os.path.join(output_dir, "val", "no_yawn")

os.makedirs(train_yawn, exist_ok=True)
os.makedirs(train_no_yawn, exist_ok=True)
os.makedirs(val_yawn, exist_ok=True)
os.makedirs(val_no_yawn, exist_ok=True)

def split_and_copy(src_folder, train_folder, val_folder):
    files = [f for f in os.listdir(src_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(files)
    split_idx = int(len(files) * train_ratio)
    train_files = files[:split_idx]
    val_files = files[split_idx:]

    for f in train_files:
        shutil.copy(os.path.join(src_folder, f), os.path.join(train_folder, f))
    for f in val_files:
        shutil.copy(os.path.join(src_folder, f), os.path.join(val_folder, f))

    return len(train_files), len(val_files)

train_y, val_y = split_and_copy(yawn_dir, train_yawn, val_yawn)
train_ny, val_ny = split_and_copy(no_yawn_dir, train_no_yawn, val_no_yawn)

print(f"Yawn: {train_y} train, {val_y} val")
print(f"No_yawn: {train_ny} train, {val_ny} val")
print(f"Split dataset saved to: {output_dir}")
