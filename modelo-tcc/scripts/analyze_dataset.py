import os
import yaml
import glob
from collections import defaultdict, Counter

def analyze_dataset(base_path):
    data_yaml_path = os.path.join(base_path, 'data.yaml')
    
    with open(data_yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    print(f"Dataset Configuration:")
    print(f"  Classes ({data['nc']}): {data['names']}")
    
    lesion_classes = {0, 1} # Lesao no quarto dianteiro, Lesao no quarto traseiro
    loss_classes = {2, 3}   # Perda no quarto dianteiro, Perda no quarto traseiro
    
    subsets = ['train', 'valid', 'test']
    
    image_types = Counter()
    total_images_with_labels = 0
    
    # Track class counts
    total_labels = 0
    class_counts = Counter()

    for subset in subsets:
        labels_path = os.path.join(base_path, subset, 'labels')
        labels = glob.glob(os.path.join(labels_path, '*.txt'))
        
        for label_file in labels:
            has_lesion = False
            has_loss = False
            
            with open(label_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        class_id = int(line.split()[0])
                        # Count classes
                        class_counts[class_id] += 1
                        total_labels += 1
                        
                        if class_id in lesion_classes:
                            has_lesion = True
                        elif class_id in loss_classes:
                            has_loss = True
                    except (ValueError, IndexError):
                        pass
            
            if has_lesion and has_loss:
                image_types['Both (Lesion + Loss)'] += 1
            elif has_lesion:
                image_types['Only Lesion'] += 1
            elif has_loss:
                image_types['Only Loss'] += 1
            else:
                image_types['Empty/Unknown'] += 1
                
            total_images_with_labels += 1

    print("\n" + "="*30)
    print("Class Count Analysis (All Subsets):")
    print(f"  Total Labels: {total_labels}")
    for class_id, count in class_counts.items():
        class_name = data['names'][class_id] if class_id < len(data['names']) else f"Unknown({class_id})"
        print(f"    {class_name}: {count}")

    print("\n" + "="*30)
    print("Image Composition Analysis (All Subsets):")
    print(f"  Total Images Analyzed: {total_images_with_labels}")
    for img_type, count in image_types.items():
        percentage = (count / total_images_with_labels) * 100
        print(f"    {img_type}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/deteccao-carcacas-bovinas'
    analyze_dataset(base_path)
