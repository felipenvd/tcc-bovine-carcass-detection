from ultralytics import YOLO
import os

def train_model():
    # Load a model
    model = YOLO("yolo11m.pt")  # load a pretrained model (recommended for training)

    # Train the model
    # data: path to data.yaml
    # epochs: 100 (good starting point)
    # imgsz: 640 (standard)
    # plots: True (to see results)
    results = model.train(
        data="com-4-classes/dataset-2-classes/data.yaml",
        epochs=100,
        imgsz=1280,
        batch=16,
        name="yolo11m_1280_medium",
        project="runs/detect",
        exist_ok=True,
        device=0,
        
        # Hyperparameters (Conservative Augmentations)
        hsv_h=0.0,      # Disable Hue augmentation (color is critical)
        hsv_s=0.0,      # Disable Saturation augmentation
        hsv_v=0.2,      # Small Brightness variation
        degrees=5.0,    # Minimal rotation
        scale=0.2,      # Minimal scaling
        mosaic=0.0,     # Disable Mosaic (confusing for carcasses)
        erasing=0.0,    # Disable random erasing (don't hide lesions)
    )

if __name__ == "__main__":
    train_model()
