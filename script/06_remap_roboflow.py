import os
import glob

# --- CONFIGURATION ---
# Base path for your Roboflow data
ROBOFLOW_BASE_DIR = r"D:\Projects\HACK2SKILL\disaster.v1i.yolov8"
SUB_FOLDERS = ['train', 'valid', 'test']

# Class Mapping:
# Roboflow '0' (Damage/Rubble) -> Your Project '1' (Rubble)
CLASS_MAP = { 0: 1 }

def remap_all_folders():
    total_remapped = 0
    
    if not os.path.exists(ROBOFLOW_BASE_DIR):
        print(f"❌ ERROR: Base path not found: {ROBOFLOW_BASE_DIR}")
        return

    print(f"🚀 Starting global remap in: {ROBOFLOW_BASE_DIR}")

    for folder in SUB_FOLDERS:
        label_path = os.path.join(ROBOFLOW_BASE_DIR, folder, "labels")
        
        if not os.path.exists(label_path):
            print(f"⚠️ Skipping missing folder: {label_path}")
            continue
            
        txt_files = glob.glob(os.path.join(label_path, "*.txt"))
        folder_count = 0
        
        for file_path in txt_files:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                
                # Check the first number (the class ID)
                old_class_id = int(parts[0])
                
                if old_class_id in CLASS_MAP:
                    new_class_id = CLASS_MAP[old_class_id]
                    # Rebuild the line with the new ID and the original coordinates
                    new_line = f"{new_class_id} " + " ".join(parts[1:]) + "\n"
                    new_lines.append(new_line)
                else:
                    # Keep original if it's not in the map (just in case)
                    new_lines.append(line)
            
            # Save the corrected labels back to the file
            with open(file_path, 'w') as file:
                file.writelines(new_lines)
            
            folder_count += 1
            total_remapped += 1
            
        print(f"  📂 {folder}: Remapped {folder_count} files.")

    print(f"\n✅ SUCCESS: Remapped {total_remapped} total files across all sets!")

if __name__ == "__main__":
    remap_all_folders()