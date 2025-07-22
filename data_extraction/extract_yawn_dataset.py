import zipfile
import os

zip_path = r"C:\Users\dell\Downloads\Yawn Dataset.zip"
extract_path = r"C:\Users\dell\Downloads\yawn_dataset"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print(f"Yawn dataset extracted to: {extract_path}")
