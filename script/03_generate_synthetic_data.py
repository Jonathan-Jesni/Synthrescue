import bpy
import bpy_extras
import os
import random
import math

# --- CONFIGURATION ---
# Updated to match your Synthrescue subfolder structure
OUTPUT_DIR = r"D:\Projects\HACK2SKILL\Synthrescue\dataset"
NUM_IMAGES_TO_GENERATE = 1000 # Increased for better generalization
CAMERA_HEIGHT = 15.0
SCATTER_RADIUS = 4.0

os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "labels"), exist_ok=True)

def setup_lighting():
    """Adds a strong sun lamp over the new stage."""
    if 'DroneSun' not in bpy.data.objects:
        light_data = bpy.data.lights.new(name="DroneSun", type='SUN')
        light_data.energy = 5.0 # Bright sunlight
        light_obj = bpy.data.objects.new(name="DroneSun", object_data=light_data)
        bpy.context.scene.collection.objects.link(light_obj)
    else:
        light_obj = bpy.data.objects['DroneSun']
        
    light_obj.location = (100, 100, 20)
    light_obj.rotation_euler = (0, 0, 0) # Point straight down

def setup_drone_camera():
    if 'DroneCam' not in bpy.data.objects:
        cam_data = bpy.data.cameras.new('DroneCam')
        cam_obj = bpy.data.objects.new('DroneCam', cam_data)
        bpy.context.scene.collection.objects.link(cam_obj)
    else:
        cam_obj = bpy.data.objects['DroneCam']
    
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (100, 100, CAMERA_HEIGHT) 
    cam_obj.rotation_euler = (0, 0, 0)
    
    bpy.context.scene.render.resolution_x = 640
    bpy.context.scene.render.resolution_y = 640
    return cam_obj

def get_yolo_bbox(scene, cam_obj, obj):
    if not obj.data or not obj.data.vertices:
        return None
        
    vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
    coords_2d = [bpy_extras.object_utils.world_to_camera_view(scene, cam_obj, v) for v in vertices]
    
    if any(c.z <= 0.0 for c in coords_2d): return None

    min_x = min([c.x for c in coords_2d])
    max_x = max([c.x for c in coords_2d])
    min_y = min([c.y for c in coords_2d])
    max_y = max([c.y for c in coords_2d])
    
    min_x, max_x = max(0.0, min_x), min(1.0, max_x)
    min_y, max_y = max(0.0, min_y), min(1.0, max_y)
    
    width = max_x - min_x
    height = max_y - min_y
    
    if width <= 0.01 or height <= 0.01: return None
        
    x_center = min_x + (width / 2.0)
    y_center = 1.0 - (min_y + (height / 2.0))
    
    return f"{obj['yolo_class']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

def generate_dataset():
    scene = bpy.context.scene
    setup_lighting()
    cam_obj = setup_drone_camera()
    
    col_survivors = bpy.data.collections.get("YOLO_0_Survivors")
    col_debris = bpy.data.collections.get("YOLO_1_Debris")
    col_ignore = bpy.data.collections.get("YOLO_Ignore_Environment")
    
    if not col_survivors or not col_debris:
        print("Error: Missing YOLO collections!")
        return

    if col_survivors: col_survivors.hide_render = True
    if col_debris: col_debris.hide_render = True
    if col_ignore: col_ignore.hide_render = False 

    if "Active_Scatter" in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections["Active_Scatter"])
    active_col = bpy.data.collections.new("Active_Scatter")
    scene.collection.children.link(active_col)

    for i in range(NUM_IMAGES_TO_GENERATE):
        print(f"Generating image {i+1}/{NUM_IMAGES_TO_GENERATE}...")
        
        for obj in active_col.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
            
        labels = []
        
        if col_survivors.objects:
            base_survivor = random.choice(col_survivors.objects)
            new_survivor = base_survivor.copy()
            new_survivor.data = base_survivor.data.copy()
            active_col.objects.link(new_survivor)
            
            s_x = 100 + random.uniform(-SCATTER_RADIUS, SCATTER_RADIUS)
            s_y = 100 + random.uniform(-SCATTER_RADIUS, SCATTER_RADIUS)
            
            new_survivor.location = (s_x, s_y, 0.05) 
            new_survivor.rotation_euler = (0, 0, random.uniform(0, math.pi*2))
            
            bpy.context.view_layer.update()
            bbox = get_yolo_bbox(scene, cam_obj, new_survivor)
            if bbox: labels.append(bbox)
            
            # --- START HEAVY OCCLUSION LOGIC ---
            num_debris = random.randint(5, 12) # Increased debris count
            for j in range(num_debris):
                if not col_debris.objects: break
                base_debris = random.choice(col_debris.objects)
                new_debris = base_debris.copy()
                new_debris.data = base_debris.data.copy()
                active_col.objects.link(new_debris)
                
                # First 3 pieces are forced to "bury" the survivor
                offset = 0.6 if j < 3 else 2.0 
                
                new_debris.location = (
                    s_x + random.uniform(-offset, offset),
                    s_y + random.uniform(-offset, offset),
                    random.uniform(0.1, 0.8) # Lower Z height for partial burial
                )
                new_debris.rotation_euler = (random.uniform(0, 6), random.uniform(0, 6), random.uniform(0, 6))
                
                bpy.context.view_layer.update()
                bbox = get_yolo_bbox(scene, cam_obj, new_debris)
                if bbox: labels.append(bbox)
            # --- END HEAVY OCCLUSION LOGIC ---
        
        img_path = os.path.join(OUTPUT_DIR, "images", f"frame_{i:04d}.jpg")
        txt_path = os.path.join(OUTPUT_DIR, "labels", f"frame_{i:04d}.txt")
        
        scene.render.filepath = img_path
        bpy.ops.render.render(write_still=True)
        
        with open(txt_path, 'w') as f:
            f.write('\n'.join(labels))
            
    print("Dataset generation complete!")

generate_dataset()