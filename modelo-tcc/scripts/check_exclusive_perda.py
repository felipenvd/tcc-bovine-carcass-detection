import os
import glob
from collections import Counter

def analyze_perda_traseira_exclusive(base_path):
    # Class ID 3 is 'Perda no quarto traseiro' based on data.yaml names order:
    # ['Lesao no quarto dianteiro', 'Lesao no quarto traseiro', 'Perda no quarto dianteiro', 'Perda no quarto traseiro']
    PERDA_TRASEIRA_ID = 3
    
    subsets = ['train'] # We usually only balance the training set
    
    exclusive_count = 0
    exclusive_annotations = 0
    total_images = 0
    
    for subset in subsets:
        labels_path = os.path.join(base_path, subset, 'labels')
        labels = glob.glob(os.path.join(labels_path, '*.txt'))
        
        for label_file in labels:
            total_images += 1
            is_exclusive = True
            has_perda_traseira = False
            
            with open(label_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    is_exclusive = False # Empty file
                
                for line in lines:
                    try:
                        class_id = int(line.split()[0])
                        if class_id == PERDA_TRASEIRA_ID:
                            has_perda_traseira = True
                        else:
                            is_exclusive = False # Contains another class
                            break
                    except (ValueError, IndexError):
                        pass
            
            if is_exclusive and has_perda_traseira:
                exclusive_count += 1
                # Count lines in files which equals number of annotations
                with open(label_file, 'r') as f:
                    exclusive_annotations += len(f.readlines())
                
    print(f"Analysis of 'Perda no quarto traseiro' (Class ID 3) in TRAIN set:")
    print(f"  Total Training Images: {total_images}")
    print(f"  Images containing ONLY 'Perda no quarto traseiro': {exclusive_count}")
    print(f"  Total Annotations in these images: {exclusive_annotations}")

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/deteccao-carcacas-bovinas'
    analyze_perda_traseira_exclusive(base_path)
