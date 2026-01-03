import cv2
import os
import glob
import random

def visualize_sample(base_path):
    # Find generated augmented images
    train_images_path = os.path.join(base_path, 'train', 'images')
    train_labels_path = os.path.join(base_path, 'train', 'labels')
    
    # Look for our heavy augmentations
    aug_images = glob.glob(os.path.join(train_images_path, 'aug_heavy_*.jpg'))
    
    if not aug_images:
        print("No augmented images found.")
        return

    # Pick a random one
    img_path = random.choice(aug_images)
    filename = os.path.basename(img_path)
    label_filename = os.path.splitext(filename)[0] + '.txt'
    label_path = os.path.join(train_labels_path, label_filename)
    
    print(f"Visualizing: {filename}")
    
    # Load Image
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    
    # Load Labels
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:
                    cls_id = int(parts[0])
                    cx, cy, bw, bh = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                    
                    # YOLO to Pixels
                    x1 = int((cx - bw/2) * w)
                    y1 = int((cy - bh/2) * h)
                    x2 = int((cx + bw/2) * w)
                    y2 = int((cy + bh/2) * h)
                    
                    # Draw Color based on Class
                    color = (0, 255, 0) if cls_id == 0 else (0, 0, 255) # Green for Lesion, Red for Loss
                    label_name = "Lesion" if cls_id == 0 else "Loss"
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(img, label_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    # Save output
    output_path = 'visualization_check_augmented.jpg'
    cv2.imwrite(output_path, img)
    print(f"Saved augmented visualization to: {os.path.abspath(output_path)}")

    # ---------------------------------------------------------
    # Now find and visualize the original
    # ---------------------------------------------------------
    # Format: aug_heavy_{i}_{original_name_no_ext}
    # Example: aug_heavy_9_7-2-video16141...
    
    # Remove prefix "aug_heavy_"
    parts = filename.split('_', 3) # split "aug", "heavy", "9", "rest"
    if len(parts) >= 4:
        # Reconstruct original root name. It might actually be simpler:
        # The script used: new_name = f"{prefix}{i}_{name_root}"
        # So we just need to find where the original name starts.
        
        # Heuristic: The original filenames don't start with aug_heavy.
        # Let's try to match the suffix in the folder.
        
        # Actually, simpler:
        # We know the logic: prefix is "aug_heavy_" or "aug_light_"
        # followed by a number, then an underscore.
        
        prefix_identifiers = ["aug_heavy_", "aug_light_"]
        current_id = ""
        for pid in prefix_identifiers:
            if filename.startswith(pid):
                current_id = pid
                break
        
        if current_id:
            rest = filename[len(current_id):] # "9_original-name.jpg" or "9_original-name" (filename has ext?)
            # The filename variable comes from os.path.basename which includes extension .jpg
            # But the 'new_name' logic appended .jpg.
            # So filename is "aug_heavy_9_foo.jpg"
            # rest is "9_foo.jpg"
            
            # Split off the index
            if '_' in rest:
                _, original_root_with_ext = rest.split('_', 1)
                # original_root_with_ext is "foo.jpg"
                
                # Check if this exists in the dir (it should!)
                original_full_path = os.path.join(train_images_path, original_root_with_ext)
                if not os.path.exists(original_full_path):
                     # Maybe extension mismatch or something?
                     # Try globbing
                     root_no_ext = os.path.splitext(original_root_with_ext)[0]
                     candidates = glob.glob(os.path.join(train_images_path, root_no_ext + ".*"))
                     if candidates:
                         original_full_path = candidates[0]
                
                if os.path.exists(original_full_path):
                    print(f"Found Original: {os.path.basename(original_full_path)}")
                    
                    # Visualize Original
                    img_orig = cv2.imread(original_full_path)
                    h, w = img_orig.shape[:2]
                    
                    # Original label
                    orig_label_name = os.path.splitext(os.path.basename(original_full_path))[0] + '.txt'
                    orig_label_path = os.path.join(train_labels_path, orig_label_name)
                    
                    if os.path.exists(orig_label_path):
                        with open(orig_label_path, 'r') as f:
                            lines = f.readlines()
                            for line in lines:
                                parts = line.strip().split()
                                if len(parts) == 5:
                                    cls_id = int(parts[0])
                                    cx, cy, bw, bh = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                                    x1 = int((cx - bw/2) * w)
                                    y1 = int((cy - bh/2) * h)
                                    x2 = int((cx + bw/2) * w)
                                    y2 = int((cy + bh/2) * h)
                                    color = (0, 255, 0) if cls_id == 0 else (0, 0, 255)
                                    label_name = "Lesion" if cls_id == 0 else "Loss"
                                    cv2.rectangle(img_orig, (x1, y1), (x2, y2), color, 2)
                                    cv2.putText(img_orig, label_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                    
                    output_orig_path = 'visualization_check_original.jpg'
                    cv2.imwrite(output_orig_path, img_orig)
                    print(f"Saved original visualization to: {os.path.abspath(output_orig_path)}")
                else:
                    print("Could not locate original file.")

if __name__ == "__main__":
    base_path = '/home/fnvid/Projects/verdadeiro-tcc/com-4-classes/dataset-2-classes'
    visualize_sample(base_path)
