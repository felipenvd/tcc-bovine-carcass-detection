import os
import glob
from collections import Counter
import yaml

def verify_2_classes(base_path):
    print(f"Verifying dataset at: {base_path}")
    
    subsets = ['train', 'valid', 'test']
    class_counts = Counter()
    total_labels = 0
    
    for subset in subsets:
        labels_path = os.path.join(base_path, subset, 'labels')
        labels = glob.glob(os.path.join(labels_path, '*.txt'))
        
        subset_counts = Counter()
        
        for label_file in labels:
            with open(label_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        cls_id = int(line.split()[0])
                        class_counts[cls_id] += 1
                        subset_counts[cls_id] += 1
                        total_labels += 1
                    except: pass
        
        print(f"\nSubset: {subset} ({len(labels)} files)")
        for cls, count in subset_counts.items():
            name = "Lesão" if cls == 0 else "Perda" if cls == 1 else f"Unknown({cls})"
            print(f"  {name} ({cls}): {count}")

    print("\n" + "="*30)
    print("Total Distribution (2 Classes):")
    for cls, count in class_counts.items():
        name = "Lesão" if cls == 0 else "Perda" if cls == 1 else f"Unknown({cls})"
        print(f"  {name} ({cls}): {count}")

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/dataset-2-classes'
    verify_2_classes(base_path)
