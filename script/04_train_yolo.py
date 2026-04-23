from ultralytics import YOLO

def train_production_v2():
    # 1. Load the pre-trained Nano model (Optimal for real-time drone latency)
    model = YOLO('yolov8n.pt') 

    # 2. Start the Phase 2 Training Loop
    results = model.train(
        data=r'D:\Projects\HACK2SKILL\Synthrescue\dataset\data.yaml',
        epochs=100,           
        patience=25,          # Stops if no improvement for 25 epochs
        imgsz=640,            # Matches Roboflow resize
        batch=-1,             # 🔥 AUTO-TUNE for your RTX 5050 VRAM
        device=0,             
        name='synth_rescue_v2_production',
        workers=4,            # Slightly higher for 3rd-gen laptop CPUs
        exist_ok=True,        # Overwrites the folder if you restart
        pretrained=True       # Uses COCO weights for faster convergence
    )

    # 3. Final Production Evaluation
    metrics = model.val()
    
    # Grab recall specifically for your 'Trapped_Person' (Class 0)
    # Using .float() ensure compatibility with standard python print formatting
    recall_person = metrics.box.r[0] 
    
    # Grab the mean recall (mR) for the whole system
    mean_recall = metrics.results_dict['metrics/recall(B)']

    print(f"\n--- PRODUCTION METRICS ---")
    print(f"Trapped_Person Recall: {recall_person:.4f}")
    print(f"Dataset Mean Recall:   {mean_recall:.4f}")
    print(f"---------------------------\n")

if __name__ == '__main__':
    train_production_v2()