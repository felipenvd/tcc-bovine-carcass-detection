import os
import csv
from ultralytics import YOLO

def analyze_single_experiment():
    exp_name = "yolo11m_1280_medium"
    base_path = "runs/detect"
    data_path = "/home/fnvid/Projects/RESULTADOS/verdadeiro-tcc-sem-under/com-4-classes/dataset-2-classes/data_local.yaml"
    
    print(f"{'Experiment':<25} | {'mAP50':<8} | {'mAP50-95':<8} | {'L. Recall':<10} | {'P. Recall':<10} | {'Prec.':<8}")
    print("-" * 120)

    exp_dir = os.path.join(base_path, exp_name)
    weights_path = os.path.join(exp_dir, "weights", "best.pt")
    
    try:
        # Load model
        model = YOLO(weights_path)
        
        # Run validation
        metrics = model.val(data=data_path, split='test', verbose=False, device=0)
        
        map50 = metrics.box.map50
        map50_95 = metrics.box.map
        precision = metrics.box.mp
        recall = metrics.box.mr
        
        lesao_recall = metrics.box.r[0] if len(metrics.box.r) > 0 else 0
        perda_recall = metrics.box.r[1] if len(metrics.box.r) > 1 else 0

        # Confusion Matrix Extraction
        tp_lesao = 0
        confused_with_perda = 0
        fn_background = 0
        total_gt_lesao = 0
        
        try:
            cm = metrics.confusion_matrix.matrix
            # Class 0 is Lesao.
            tp_lesao = int(cm[0, 0])
            confused_with_perda = int(cm[0, 1])
            fn_background = int(cm[0, 2]) 
            
            total_gt_lesao = tp_lesao + confused_with_perda + fn_background
            
            print(f"    [Lesao Details] TP: {tp_lesao} | Confused w/ Perda: {confused_with_perda} | Missed (FN): {fn_background} | Total GT: {total_gt_lesao}")
            
        except Exception as e:
            print(f"    Could not extract detailed CM: {e}")

        print(f"{exp_name:<25} | {map50:.4f}   | {map50_95:.4f}   | {lesao_recall:.4f}     | {perda_recall:.4f}     | {precision:.4f}")
        
    except Exception as e:
        print(f"Error analyzing {exp_name}: {e}")

if __name__ == "__main__":
    analyze_single_experiment()
