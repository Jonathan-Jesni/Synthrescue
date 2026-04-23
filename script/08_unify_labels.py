import os

# MASTER PATH
DATASET_LABELS = r"D:\Projects\HACK2SKILL\Synthrescue\dataset\labels"

def unify_to_survivor():
    count = 0
    for root, _, files in os.walk(DATASET_LABELS):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    lines = f.readlines()
                
                # Force the first number of every line to '0' (Survivor)
                fixed_lines = ["0 " + " ".join(line.split()[1:]) + "\n" for line in lines if line.strip()]
                
                with open(path, 'w') as f:
                    f.writelines(fixed_lines)
                count += 1
    print(f"✅ SUCCESS: Unified {count} files. All detections are now Class 0 (Survivor).")

if __name__ == "__main__":
    unify_to_survivor()