import os
import zipfile
import pydicom
import numpy as np
from PIL import Image
from pathlib import Path
import shutil

INPUT_DIR = Path("Images")  
OUTPUT_DIR = Path("OUTPUT/JPG_OUT_ORDERED")
TEMP_EXTRACT_DIR = Path("OUTPUT/temp_extracted")

def normalize_image(pixel_array):
    image_float = pixel_array.astype(float)
    min_val = np.min(image_float)
    max_val = np.max(image_float)
    if max_val - min_val == 0:
        return np.zeros(image_float.shape, dtype=np.uint8)
    scaled_image = (np.maximum(image_float, 0) / max_val) * 255.0
    return np.uint8(scaled_image)


def process_single_dicom(dcm_path, base_input_path, target_output_root, parent_label):
    try:
        dicom_data = pydicom.dcmread(dcm_path)
        if not hasattr(dicom_data, 'pixel_array'):
            return False

        relative_inner_path = dcm_path.relative_to(base_input_path)
        
        output_file_path = target_output_root / parent_label / relative_inner_path
        output_file_path = output_file_path.with_suffix('.jpg')
        
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        normalized_pixels = normalize_image(dicom_data.pixel_array)
        image = Image.fromarray(normalized_pixels)
        image.save(output_file_path)
        return True
    except Exception as e:
        return False
    

def convert_dicom_directory():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    success_count = 0

    # 1. HANDLE ZIP FILES
    zip_files = list(INPUT_DIR.glob('*.zip'))
    for zip_path in zip_files:
        parent_name = zip_path.stem
        print(f"Processing ZIP: {parent_name}")
        
        zip_extract_to = TEMP_EXTRACT_DIR / parent_name
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(zip_extract_to)
            
            for dcm_path in zip_extract_to.rglob('*'):
                if dcm_path.is_file():
                    if process_single_dicom(dcm_path, zip_extract_to, OUTPUT_DIR, parent_name):
                        success_count += 1
        except Exception as e:
            print(f"Failed ZIP {zip_path.name}: {e}")

    # 2. HANDLE REGULAR FOLDERS
    for study_folder in INPUT_DIR.iterdir():
        if study_folder.is_dir() and study_folder != TEMP_EXTRACT_DIR:
            parent_name = study_folder.name
            print(f"Processing Folder: {parent_name}")
            
            for dcm_path in study_folder.rglob('*'):
                if dcm_path.is_file() and dcm_path.suffix.lower() in ['.dcm', '']:
                    if process_single_dicom(dcm_path, study_folder, OUTPUT_DIR, parent_name):
                        success_count += 1

    if TEMP_EXTRACT_DIR.exists():
        shutil.rmtree(TEMP_EXTRACT_DIR)

    print(f"\n--- Done! Saved {success_count} slices to {OUTPUT_DIR} ---")

if __name__ == "__main__":
    convert_dicom_directory()