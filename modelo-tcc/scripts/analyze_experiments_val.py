import os
import csv
from ultralytics import YOLO

def analyze_experiments():
    base_path = "runs/detect"
    experiments = [
        "yolo11n_896_nano", "yolo11n_1024_nano", "yolo11n_1280_nano",
        "yolo11s_896_small", "yolo11s_1024_small", "yolo11s_1280_small",
        "yolo11m_896_medium", "yolo11m_1024_medium", "yolo11m_1280_medium"
    ]

    # Updated data path relative to script execution location (modelo-tcc/)
    data_path = "dataset/dataset-2-classes/data_local.yaml"
    
    results = []

    print(f"{'Experiment':<25} | {'mAP50':<8} | {'mAP50-95':<8} | {'L. Recall':<10} | {'P. Recall':<10} | {'Prec.':<8}")
    print("-" * 120)

    for exp_name in experiments:
        exp_dir = os.path.join(base_path, exp_name)
        weights_path = os.path.join(exp_dir, "weights", "best.pt")
        
        if not os.path.exists(weights_path):
            print(f"Skipping {exp_name}: best.pt not found.")
            continue

        try:
            # Load model
            model = YOLO(weights_path)
            
            # Run validation on VAL split
            metrics = model.val(data=data_path, split='val', verbose=False, device='cpu')
            
            map50 = metrics.box.map50
            map50_95 = metrics.box.map
            precision = metrics.box.mp
            recall = metrics.box.mr
            
            lesao_recall = metrics.box.r[0] if len(metrics.box.r) > 0 else 0
            perda_recall = metrics.box.r[1] if len(metrics.box.r) > 1 else 0

            print(f"{exp_name:<25} | {map50:.4f}   | {map50_95:.4f}   | {lesao_recall:.4f}     | {perda_recall:.4f}     | {precision:.4f}")
            
            results.append({
                "Experiment": exp_name,
                "mAP50": map50,
                "mAP50-95": map50_95,
                "Lesao Recall": lesao_recall,
                "Perda Recall": perda_recall,
                "Precision": precision
            })
            
        except Exception as e:
            print(f"Error analyzing {exp_name}: {e}")

    # Save to CSV
    if results:
        keys = results[0].keys()
        with open("experiment_comparison_results_val.csv", "w", newline="") as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        print("\nResults saved to experiment_comparison_results_val.csv")

if __name__ == "__main__":
    analyze_experiments()
