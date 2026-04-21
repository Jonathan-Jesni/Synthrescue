# SynthRescue: Synthetic Object Detection for Disaster Relief

## Objective
SynthRescue is an end-to-end computer vision pipeline designed to locate trapped survivors in disaster zones using drone-perspective imagery. The project utilizes procedurally generated synthetic data to train a YOLOv8 model for high-recall performance in complex, occluded environments.

## Technical Architecture
### 1. Synthetic Data Generation (Blender)
- **Procedural Placement**: Scripts automate the import and organization of low-poly assets.
- **Heavy Occlusion Logic**: Implemented "High-Burial" simulation to increase model recall for partially covered survivors.
- **Visual Contrast**: Applied high-visibility Neon Green to survivors and Terracotta Red to rubble to resolve feature collision issues.

### 2. Machine Learning Pipeline
- **Dataset**: 1,000 procedurally rendered images with a professional 80/20 train/test split.
- **Model**: YOLOv8n (Nano) optimized for real-time drone deployment.
- **Hardware**: Trained on NVIDIA GeForce RTX 5050 Laptop GPU.

## Project Structure
- `/dataset`: Subdivided into `train` and `val` sets with corresponding YOLO labels.
- `/models`: 3D asset library for disaster simulation.
- `/script`: Python automation scripts for the full data-to-training loop.

## Key Metrics
- **Target Recall**: 0.95 for Class: Trapped_Person.
- **Innovation**: Eliminates the need for manual labeling by using Blender's coordinate system to export perfect bounding boxes.