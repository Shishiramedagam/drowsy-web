{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "5444e086",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Datasets extracted successfully!\n"
     ]
    }
   ],
   "source": [
    "import zipfile\n",
    "import os\n",
    "\n",
    "# Paths to your local downloaded zip files\n",
    "eye_zip = r\"C:\\Users\\dell\\Downloads\\Eye dataset.zip\"\n",
    "yawn_zip = r\"C:\\Users\\dell\\Downloads\\yawdd.v1i.tensorflow.zip\"\n",
    "\n",
    "# Extraction directories\n",
    "extract_eye = r\"C:\\Users\\dell\\Downloads\\drowsiness_data\\eye_dataset\"\n",
    "extract_yawn = r\"C:\\Users\\dell\\Downloads\\drowsiness_data\\yawn_dataset\"\n",
    "\n",
    "# Create directories if they don't exist\n",
    "os.makedirs(extract_eye, exist_ok=True)\n",
    "os.makedirs(extract_yawn, exist_ok=True)\n",
    "\n",
    "# Unzip Eye dataset\n",
    "with zipfile.ZipFile(eye_zip, 'r') as zip_ref:\n",
    "    zip_ref.extractall(extract_eye)\n",
    "\n",
    "# Unzip Yawning dataset\n",
    "with zipfile.ZipFile(yawn_zip, 'r') as zip_ref:\n",
    "    zip_ref.extractall(extract_yawn)\n",
    "\n",
    "print(\"Datasets extracted successfully!\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
