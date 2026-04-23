import os
import shutil
import glob

# --- CONFIGURATION ---
ROBOFLOW_SRC = r"D:\Projects\HACK2SKILL\disaster.v1i.yolov8"
SYNTH_DEST = r"D:\Projects\HACK2SKILL\Synthrescue\dataset"

# Mapping: (Source Subfolder, Destination Subfolder)
# Merging both 'valid' and 'test' into your single 'val' folder for a stronger validation set.
MAPPING = [
    ('train', 'train'),
    ('valid', 'val'),
    ('test', 'val')
]

def migrate_roboflow_data():
    total_moved = 0
    
    if not os.path.exists(ROBOFLOW_SRC) or not os.path.exists(SYNTH_DEST):
        print("❌ ERROR: Ensure both source and destination paths exist.")
        return

    print(f"🚀 Starting migration to {SYNTH_DEST}...")

    for src_sub, dest_sub in MAPPING:
        # Paths for Images
        src_img_path = os.path.join(ROBOFLOW_SRC, src_sub, "images")
        dest_img_path = os.path.join(SYNTH_DEST, "images", dest_sub)
        
        # Paths for Labels
        src_lbl_path = os.path.join(ROBOFLOW_SRC, src_sub, "labels")
        dest_lbl_path = os.path.join(SYNTH_DEST, "labels", dest_sub)
        
        # Safety check for source folders
        if not os.path.exists(src_img_path) or not os.path.exists(src_lbl_path):
            print(f"⚠️ Skipping {src_sub}: Folders not found.")
            continue

        # Move Images (Handling .jpg and .png)
        img_count = 0
        for ext in ['*.jpg', '*.png', '*.jpeg']:
            for img_file in glob.glob(os.path.join(src_img_path, ext)):
                shutil.move(img_file, os.path.join(dest_img_path, os.path.basename(img_file)))
                img_count += 1
                total_moved += 1
                
        # Move Labels (.txt)
        lbl_count = 0
        for lbl_file in glob.glob(os.path.join(src_lbl_path, "*.txt")):
            shutil.move(lbl_file, os.path.join(dest_lbl_path, os.path.basename(lbl_file)))
            lbl_count += 1
            total_moved += 1
            
        print(f"  📂 {src_sub} -> {dest_sub}: Moved {img_count} images and {lbl_count} labels.")

    print(f"\n✅ SUCCESS: Integrated {total_moved} real-world files into the hybrid dataset!")

if __name__ == "__main__":
    migrate_roboflow_data()