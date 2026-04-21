from ultralytics import YOLO

def train_production_v2():
    # 1. Load the pre-trained Nano model as a baseline
    model = YOLO('yolov8n.pt') 

    # 2. Start the Phase 2 Training Loop
    # We increase epochs to 100 to allow the model to learn the harder occlusions.
    # 'patience' stops training if the model stops improving for 25 epochs.
    results = model.train(
        data=r'D:\Projects\HACK2SKILL\Synthrescue\dataset\data.yaml',
        epochs=100,           # Increased for production quality
        patience=25,          # Early stopping for optimization
        imgsz=640,
        device=0,             # Target your RTX 5050
        name='synth_rescue_v2_production',
        workers=2             # Optimized for Windows multiprocessing stability
    )

    # 3. Final Production Evaluation
    # This validates against the new /val subfolder for honest metrics.
    metrics = model.val()
    
    # Target: We want to see this value climb toward 0.90 - 0.95
    recall_person = metrics.results_dict['metrics/recall(B)']
    print(f"\n--- PRODUCTION METRICS ---")
    print(f"Final Recall for Trapped_Person: {recall_person:.4f}")
    print(f"---------------------------\n")

if __name__ == '__main__':
    train_production_v2()