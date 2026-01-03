import os
import glob
import shutil

def undersample_perda_traseira(base_path):
    # Class ID 3 is 'Perda no quarto traseiro'
    PERDA_TRASEIRA_ID = 3
    
    # We only remove from train
    subset = 'train'
    
    images_path = os.path.join(base_path, subset, 'images')
    labels_path = os.path.join(base_path, subset, 'labels')
    
    # Create backup directory for removed files
    backup_dir = os.path.join(base_path, 'undersampled_backup')
    os.makedirs(os.path.join(backup_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(backup_dir, 'labels'), exist_ok=True)
    
    print(f"Scanning {labels_path}...")
    
    labels = glob.glob(os.path.join(labels_path, '*.txt'))
    removed_count = 0
    
    for label_file in labels:
        is_exclusive = True
        has_perda_traseira = False
        
        # Check content
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
            # It's an exclusive file. Move it and its image.
            
            # 1. Move Label
            filename = os.path.basename(label_file)
            shutil.move(label_file, os.path.join(backup_dir, 'labels', filename))
            
            # 2. Find and Move Image
            # Image could be .jpg, .jpeg, .png. Assuming same basename.
            image_basename = os.path.splitext(filename)[0]
            # Try extensions
            for ext in ['.jpg', '.jpeg', '.png', '.JPG']:
                image_file = os.path.join(images_path, image_basename + ext)
                if os.path.exists(image_file):
                    shutil.move(image_file, os.path.join(backup_dir, 'images', image_basename + ext))
                    break
            
            removed_count += 1
            print(f"Removed: {filename}")

    print("\n" + "="*30)
    print(f"Undersampling Complete.")
    print(f"Total images removed: {removed_count}")
    print(f"Files moved to: {backup_dir}")

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/deteccao-carcacas-bovinas'
    undersample_perda_traseira(base_path)
