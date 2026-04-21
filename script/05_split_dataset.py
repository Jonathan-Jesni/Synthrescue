import os
import random
import shutil

# --- CONFIGURATION ---
DATASET_PATH = r"D:\Projects\HACK2SKILL\Synthrescue\dataset"
IMAGES_SRC = os.path.join(DATASET_PATH, "images")
LABELS_SRC = os.path.join(DATASET_PATH, "labels")

def perform_split():
    if not os.path.exists(IMAGES_SRC):
        print(f"❌ ERROR: Path does not exist: {IMAGES_SRC}")
        return

    all_files = os.listdir(IMAGES_SRC)
    
    # Updated to look for .png files
    all_frames = [f.split('.')[0] for f in all_files if f.lower().endswith('.png')]
    
    # Ensure matching label exists
    valid_frames = [f for f in all_frames if os.path.exists(os.path.join(LABELS_SRC, f + ".txt"))]
    random.shuffle(valid_frames)

    if not valid_frames:
        print("⚠️ Still 0 valid pairs found. Check your labels folder.")
        return

    # Create standard YOLO subfolder structure
    for folder in ["train", "val"]:
        os.makedirs(os.path.join(IMAGES_SRC, folder), exist_ok=True)
        os.makedirs(os.path.join(LABELS_SRC, folder), exist_ok=True)

    # Calculate 80/20 Split
    split_idx = int(len(valid_frames) * 0.8)
    train_set = valid_frames[:split_idx]
    val_set = valid_frames[split_idx:]

    def move_files(frame_list, subset):
        count = 0
        for frame in frame_list:
            # Explicitly moving .png files
            shutil.move(os.path.join(IMAGES_SRC, frame + ".png"), 
                        os.path.join(IMAGES_SRC, subset, frame + ".png"))
            shutil.move(os.path.join(LABELS_SRC, frame + ".txt"), 
                        os.path.join(LABELS_SRC, subset, frame + ".txt"))
            count += 1
        return count

    print(f"📦 Moving {len(valid_frames)} valid image/label pairs...")
    t_count = move_files(train_set, "train")
    v_count = move_files(val_set, "val")
    print(f"✅ SUCCESS: {t_count} in Train | {v_count} in Val")

if __name__ == "__main__":
    perform_split()