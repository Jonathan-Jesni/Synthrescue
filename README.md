# SynthRescue: Synthetic Object Detection for Disaster Relief

## Objective
SynthRescue is an end-to-end computer vision pipeline designed to locate trapped survivors in disaster zones using drone-perspective imagery. The project utilizes procedurally generated synthetic data to train a YOLOv8 model for high-recall performance in complex, occluded environments.

## Technical Architecture
### 1. Synthetic Data Generation (Blender)
- **Procedural Placement**: Python scripts automate the placement, rotation, and scaling of low-poly disaster assets.
- **Heavy Occlusion Logic**: Implemented "High-Burial" simulation, forcing survivors to be partially covered by 5–12 pieces of debris to increase model robustness.
- **Visual Contrast**: Applied high-visibility materials (Neon Green survivors vs. Terracotta Red rubble) to eliminate feature collision in low-poly environments.

### 2. Machine Learning Pipeline
- **Dataset**: 1,000 procedurally rendered images with a professional 80/20 train/test split.
- **Model**: YOLOv8n (Nano) optimized for high-speed edge deployment on search-and-rescue drones.
- **Hardware**: Trained on NVIDIA GeForce RTX 5050 Laptop GPU.

## Key Results (Final Production Run)
- **Survivor Recall (Class 0)**: **98.3%** (Target: 95%)
- **Survivor Precision**: **100%** (Zero false positives for trapped persons)
- **mAP50**: **0.911** across all classes

## Project Structure
- `/dataset`: YOLOv8 formatted images and labels organized into `train` and `val` sets.
- `/models`: 3D asset library including survivors and disaster debris.
- `/script`: Full automation suite including batch importers, collection organizers, and training scripts.

## Innovation
- **Zero-Manual Labeling**: Uses Blender's internal coordinate system to automatically export mathematically perfect bounding boxes, saving hundreds of manual hours.
- **Edge-Case Simulation**: Procedurally generates thousands of unique occlusion scenarios that would be impossible to capture safely in real-world disaster zones.