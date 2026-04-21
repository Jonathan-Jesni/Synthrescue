from ultralytics import YOLO

def train_production_v2():
    # 1. Load the pre-trained Nano model as a baseline
    model = YOLO('yolov8n.pt') 

    # 2. Start the Phase 2 Training Loop
    results = model.train(
        data=r'D:\Projects\HACK2SKILL\Synthrescue\dataset\data.yaml',
        epochs=100,           
        patience=25,          
        imgsz=640,
        device=0,             # Target your RTX 5050
        name='synth_rescue_v2_production',
        workers=2             
    )

    # 3. Final Production Evaluation
    metrics = model.val()
    
    # FIX: Grab recall for Class 0 (Trapped_Person) specifically
    # metrics.box.r is a list of recall values for each class
    recall_person = metrics.box.r[0] 
    
    # Grab the mean recall for comparison
    mean_recall = metrics.results_dict['metrics/recall(B)']

    print(f"\n--- PRODUCTION METRICS ---")
    print(f"Trapped_Person Recall: {recall_person:.4f}")
    print(f"Dataset Mean Recall:   {mean_recall:.4f}")
    print(f"---------------------------\n")

if __name__ == '__main__':
    train_production_v2()