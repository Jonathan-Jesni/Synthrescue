from ultralytics import YOLO

def train_production_v3():
    # 1. Load the pre-trained Nano model
    model = YOLO('yolov8n.pt') 

    # 2. Start the Phase 2 Training Loop
    results = model.train(
        data=r'D:\Projects\HACK2SKILL\Synthrescue\dataset\data.yaml',
        epochs=200,           
        patience=25,        
        imgsz=640,            
        batch=-1,             
        device=0,             
        name='synth_rescue_v3_unified', 
        workers=4,            
        exist_ok=True,        
        pretrained=True       
    )

    # 3. Final Production Evaluation
    metrics = model.val()
    
    # Grab recall specifically for your ONLY class now (Trapped_Survivor)
    recall_survivor = metrics.box.r[0] 
    
    # Grab the precision as well to show the judges how accurate it is
    precision_survivor = metrics.box.p[0]

    print(f"\n--- V3 UNIFIED PRODUCTION METRICS ---")
    print(f"Trapped_Survivor Recall:    {recall_survivor:.4f}")
    print(f"Trapped_Survivor Precision: {precision_survivor:.4f}")
    print(f"-------------------------------------\n")

if __name__ == '__main__':
    train_production_v3()