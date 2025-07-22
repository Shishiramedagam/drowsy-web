import os
import shutil

# Path to the raw Eye dataset
raw_eye_path = r"C:\Users\dell\Downloads\drowsiness_data\eye_dataset"
sorted_eye_path = r"C:\Users\dell\Downloads\drowsiness_data\sorted_eyes"

open_path = os.path.join(sorted_eye_path, "open")
closed_path = os.path.join(sorted_eye_path, "closed")

os.makedirs(open_path, exist_ok=True)
os.makedirs(closed_path, exist_ok=True)

count_open, count_closed = 0, 0

# Loop through all files and sort
for root, dirs, files in os.walk(raw_eye_path):
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg"):
            # The 5th element (0 or 1) in the filename indicates eye state
            parts = file.split('_')
            if len(parts) >= 5:
                eye_state = parts[4]  # 0 = open, 1 = closed
                src = os.path.join(root, file)
                if eye_state == "0":
                    shutil.copy(src, os.path.join(open_path, file))
                    count_open += 1
                elif eye_state == "1":
                    shutil.copy(src, os.path.join(closed_path, file))
                    count_closed += 1

print(f"Sorting complete: {count_open} open eyes, {count_closed} closed eyes.")
print(f"Sorted dataset is in: {sorted_eye_path}")
