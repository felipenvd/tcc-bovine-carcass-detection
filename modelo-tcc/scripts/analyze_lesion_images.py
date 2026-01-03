import os
import glob
from collections import Counter
from tqdm import tqdm

def analyze_lesion_images(base_path):
    print(f"Analyzing Lesion Images in: {base_path}")
    
    # Class 0 = Lesion, Class 1 = Loss
    subsets = ['train', 'valid', 'test']
    
    lesion_only_imgs = 0
    lesion_only_anns = 0
    
    mixed_imgs = 0
    mixed_anns_lesion = 0
    mixed_anns_loss = 0
    
    for subset in subsets:
        labels_path = os.path.join(base_path, subset, 'labels')
        labels = glob.glob(os.path.join(labels_path, '*.txt'))
        
        for label_file in labels:
            has_lesion = False
            has_loss = False
            lesion_count = 0
            loss_count = 0
            
            with open(label_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        cls_id = int(line.split()[0])
                        if cls_id == 0:
                            has_lesion = True
                            lesion_count += 1
                        elif cls_id == 1:
                            has_loss = True
                            loss_count += 1
                    except: pass
            
            if has_lesion and not has_loss:
                lesion_only_imgs += 1
                lesion_only_anns += lesion_count
            elif has_lesion and has_loss:
                mixed_imgs += 1
                mixed_anns_lesion += lesion_count
                mixed_anns_loss += loss_count

    print("\n" + "="*30)
    print("Lesion Image Analysis (All Subsets):")
    
    print(f"\n1. Images with ONLY Lesions:")
    print(f"   Images: {lesion_only_imgs}")
    print(f"   Lesion Annotations: {lesion_only_anns}")
    
    print(f"\n2. Images with Lesions AND Losses (Mixed):")
    print(f"   Images: {mixed_imgs}")
    print(f"   Lesion Annotations: {mixed_anns_lesion}")
    print(f"   Loss Annotations: {mixed_anns_loss}")
    
    total_lesion_anns = lesion_only_anns + mixed_anns_lesion
    print(f"\nTotal Lesion Annotations: {total_lesion_anns}")
    print("="*30)

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/dataset-2-classes'
    analyze_lesion_images(base_path)
