import os
import cv2
import glob
import shutil
import random
import numpy as np
from tqdm import tqdm

# Mapping: 
# 0 (Lesao D), 1 (Lesao T) -> 0 (Lesao)
# 2 (Perda D), 3 (Perda T) -> 1 (Perda)
CLASS_MAPPING = {0: 0, 1: 0, 2: 1, 3: 1}

def process_dataset(src_path, dst_path):
    subsets = ['train', 'valid', 'test']
    
    for subset in subsets:
        print(f"Processing {subset}...")
        
        src_images_dir = os.path.join(src_path, subset, 'images')
        src_labels_dir = os.path.join(src_path, subset, 'labels')
        
        dst_images_dir = os.path.join(dst_path, subset, 'images')
        dst_labels_dir = os.path.join(dst_path, subset, 'labels')
        
        os.makedirs(dst_images_dir, exist_ok=True)
        os.makedirs(dst_labels_dir, exist_ok=True)
        
        image_files = glob.glob(os.path.join(src_images_dir, '*'))
        
        for img_path in tqdm(image_files):
            img_name = os.path.basename(img_path)
            label_name = os.path.splitext(img_name)[0] + '.txt'
            label_path = os.path.join(src_labels_dir, label_name)
            
            if not os.path.exists(label_path):
                continue
                
            # Read Image
            img = cv2.imread(img_path)
            if img is None:
                continue
            h, w = img.shape[:2]
            
            # Read and Remap Labels
            bboxes = []
            has_lesion = False
            
            with open(label_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) != 5: continue
                    cls_id = int(parts[0])
                    
                    if cls_id not in CLASS_MAPPING: continue
                    new_cls_id = CLASS_MAPPING[cls_id]
                    
                    if new_cls_id == 0: has_lesion = True
                    
                    # Store as x,y,w,h for now
                    bboxes.append([new_cls_id] + [float(x) for x in parts[1:]])

            # Save Original (Remapped)
            shutil.copy(img_path, os.path.join(dst_images_dir, img_name))
            
            with open(os.path.join(dst_labels_dir, label_name), 'w') as f:
                for bbox in bboxes:
                    f.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]} {bbox[4]}\n")
            
            # Augmentation (DISABLED FOR NOW)
            # if subset == 'train' and has_lesion:
            #     ... logic removed ...
            pass

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/deteccao-carcacas-bovinas'
    dst_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/dataset-2-classes'
    
    print("Refactoring dataset...")
    process_dataset(base_path, dst_path)
    print("Done! Saved to", dst_path)
