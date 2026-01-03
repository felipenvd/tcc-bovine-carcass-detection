import os
import cv2
import glob
import albumentations as A
import numpy as np
from tqdm import tqdm

def get_yolo_bboxes(label_path):
    bboxes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:
                    cls_id = int(parts[0])
                    x, y, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                    bboxes.append([x, y, w, h, cls_id])
    return bboxes

def save_yolo_label(bboxes, output_path):
    with open(output_path, 'w') as f:
        for bbox in bboxes:
            # bbox is [x, y, w, h, cls_id]
            # yolo format: cls_id x y w h
            cls_id = int(bbox[4])
            x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
            f.write(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

def augment_dataset(base_path):
    print(f"Augmenting dataset at: {base_path}")
    
    # We only augment the TRAINING set
    subset = 'train'
    images_dir = os.path.join(base_path, subset, 'images')
    labels_dir = os.path.join(base_path, subset, 'labels')
    
    image_files = glob.glob(os.path.join(images_dir, '*.jpg')) + \
                  glob.glob(os.path.join(images_dir, '*.jpeg')) + \
                  glob.glob(os.path.join(images_dir, '*.png'))
    
    # 1. Heavy Augmentation Pipeline (For Pure Lesion Images)
    # Generates multiple variations: Flip, Rotate, Brightness/Contrast (Safe), Zoom
    transform_heavy = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=10, p=0.5), # Adjusted to be more realistic for hanging carcasses
        A.RandomBrightnessContrast(p=0.2),
        A.RandomScale(scale_limit=0.1, p=0.5),
        # Ensure bboxes are safe
    ], bbox_params=A.BboxParams(format='yolo', min_visibility=0.3))

    # 2. Light Augmentation Pipeline (For Mixed Images)
    # Just Horizontal Flip to double the data without distorting too much
    transform_light = A.Compose([
        A.HorizontalFlip(p=1.0), # Always flip to create one new copy
    ], bbox_params=A.BboxParams(format='yolo', min_visibility=0.3))

    generated_count = 0
    
    for img_path in tqdm(image_files):
        # Fix: Label is in labels_dir, not same dir as image
        filename = os.path.basename(img_path)
        label_filename = os.path.splitext(filename)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_filename)
        
        bboxes = get_yolo_bboxes(label_path)
        if not bboxes: continue
        
        has_lesion = any(b[4] == 0 for b in bboxes)
        has_loss = any(b[4] == 1 for b in bboxes)
        
        if not has_lesion:
            continue
            
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Decide Strategy
        if has_lesion and not has_loss:
            # Pure Lesion: HEAVY (Generate 25 variants)
            # Goal: Add ~900 annotations from these 30 images
            num_variants = 25
            pipeline = transform_heavy
            prefix = "aug_heavy_"
            
            for i in range(num_variants):
                try:
                    transformed = pipeline(image=img, bboxes=bboxes)
                    aug_img = transformed['image']
                    aug_bboxes = transformed['bboxes']
                    
                    if len(aug_bboxes) == 0: continue # Skip if bboxes were lost
                    
                    # Save
                    filename = os.path.basename(img_path)
                    name_root = os.path.splitext(filename)[0]
                    new_name = f"{prefix}{i}_{name_root}"
                    
                    output_img_path = os.path.join(images_dir, new_name + '.jpg')
                    output_label_path = os.path.join(labels_dir, new_name + '.txt')
                    
                    # Convert back to BGR for saving
                    aug_img_bgr = cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(output_img_path, aug_img_bgr)
                    save_yolo_label(aug_bboxes, output_label_path)
                    
                    generated_count += 1
                except Exception as e:
                    print(f"Error augmenting {img_path}: {e}")
        else:
            # Mixed: Skip augmentation as requested (avoids inflating Loss class)
            continue

    print("\n" + "="*30)
    print(f"Augmentation Complete.")
    print(f"New images generated: {generated_count}")

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/dataset-2-classes'
    augment_dataset(base_path)
