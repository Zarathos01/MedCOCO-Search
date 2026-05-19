import os
import cv2
import numpy as np
import logging

# --- CONFIGURATION ---
INPUT_ROOT = "OUTPUT/JPG_OUT_ORDERED"
OUTPUT_FOLDER = "OUTPUT/FINAL"
LOG_FILE = "fusion_log.txt"

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def cv2_imread_unicode(path):
    """Reads an image from a path that may contain non-ASCII characters."""
    try:
        if not os.path.exists(path):
            return None
        file_bytes = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logging.error(f"Reader Error on {os.path.basename(path)}: {e}")
        return None


def cv2_imwrite_unicode(path, img):
    """Writes an image to a path that may contain non-ASCII characters."""
    try:
        is_success, buffer = cv2.imencode(".jpg", img)
        if is_success:
            with open(path, "wb") as f:
                f.write(buffer)
            return True
        return False
    except Exception as e:
        logging.error(f"Writer Error: {e}")
        return False


def fuse_weighted_center(volume_paths):
    """Applies 0.25/0.5/0.25 fusion to the middle of a series with shape-safety."""
    n = len(volume_paths)
    if n == 0: return None
    
    mid = n // 2
    s2 = cv2_imread_unicode(volume_paths[mid])
    
    if s2 is None:
        for path in volume_paths:
            s2 = cv2_imread_unicode(path)
            if s2 is not None: break
        if s2 is None: return None
        return s2 

    s1_raw = cv2_imread_unicode(volume_paths[max(mid - 1, 0)])
    s3_raw = cv2_imread_unicode(volume_paths[min(mid + 1, n - 1)])

    if s1_raw is None or s3_raw is None:
        return s2

    h, w = s2.shape[:2]
    s1 = cv2.resize(s1_raw, (w, h)) if s1_raw.shape[:2] != (h, w) else s1_raw
    s3 = cv2.resize(s3_raw, (w, h)) if s3_raw.shape[:2] != (h, w) else s3_raw

    s1 = s1.astype(np.float32)
    s2 = s2.astype(np.float32)
    s3 = s3.astype(np.float32)

    fused = (0.25 * s1) + (0.5 * s2) + (0.25 * s3)
    return np.clip(fused, 0, 255).astype(np.uint8)


def run_fusion_process():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    saved_count = 0
    failed_count = 0

    logging.info("--- Starting Robust Recursive Fusion ---")

    if not os.path.exists(INPUT_ROOT):
        logging.error(f"INPUT_ROOT not found: {INPUT_ROOT}")
        return

    # Use os.walk to find any folder containing JPGs regardless of nesting depth
    for root, dirs, files in os.walk(INPUT_ROOT):
        # Filter for jpg files and ignore hidden system files
        jpg_files = [os.path.join(root, f) for f in files 
                     if f.lower().endswith(('.jpg', '.jpeg')) and not f.startswith('.')]
        
        if not jpg_files:
            continue

        relative_path = os.path.relpath(root, INPUT_ROOT)
        path_parts = relative_path.split(os.sep)
        
        study_name = path_parts[0] if len(path_parts) > 0 else "UnknownStudy"
        series_name = path_parts[-1] if len(path_parts) > 1 else "UnknownSeries"

        jpg_files.sort()
        
        result = fuse_weighted_center(jpg_files)
        
        if result is not None:
            # Shorten names for path safety and sanitize
            safe_study = study_name[:50]
            safe_series = series_name if len(series_name) < 30 else "..." + series_name[-20:]
            filename = f"{safe_study}_{safe_series}.jpg".replace(":", "_").replace("/", "_").replace("\\", "_")
            
            save_path = os.path.join(OUTPUT_FOLDER, filename)
            
            if cv2_imwrite_unicode(save_path, result):
                logging.info(f"SUCCESS: {filename}")
                saved_count += 1
            else:
                logging.error(f"FAIL (Write): {filename}")
                failed_count += 1
        else:
            logging.error(f"FAIL (Process): {root}")
            failed_count += 1

    logging.info(f"\nFINISH: Saved {saved_count} fused images. Total failures: {failed_count}")

if __name__ == "__main__":
    run_fusion_process()