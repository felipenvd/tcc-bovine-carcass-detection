import cv2
import numpy as np
import os
import base64
from ultralytics import YOLO

class YoloService:
    def __init__(self):
        # Paths to model files - now in backend/models/
        self.base_path = os.path.join(os.path.dirname(__file__), "models")
        self.model_path = os.path.join(self.base_path, "best.pt")
        
        print(f"Loading YOLOv11 from {self.model_path}...")
        self.model = YOLO(self.model_path)
        
        # Colors for each class (BGR format)
        self.colors = {
            'Lesao': (0, 0, 255),    # Red
            'Perda': (255, 165, 0),  # Orange
        }

    def predict(self, image: np.ndarray):
        # Run inference
        results = self.model(image)[0]
        
        parsed_results = []
        boxes_list = []
        confidences_list = []
        class_ids_list = []
        
        for box in results.boxes:
            # Get box coordinates (x1, y1, x2, y2)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0].cpu().numpy())
            class_id = int(box.cls[0].cpu().numpy())
            class_name = results.names[class_id]
            
            # Convert to x, y, w, h for compatibility
            x = int(x1)
            y = int(y1)
            w = int(x2 - x1)
            h = int(y2 - y1)
            
            parsed_results.append({
                "class": class_name,
                "confidence": confidence,
                "box": [x, y, w, h]
            })
            
            boxes_list.append([x, y, w, h])
            confidences_list.append(confidence)
            class_ids_list.append(class_id)
            
        # Create a dummy indexes list for compatibility
        indexes = np.arange(len(boxes_list)) if boxes_list else []
                
        return parsed_results, boxes_list, confidences_list, class_ids_list, indexes

    def draw_detections(self, image: np.ndarray, boxes, confidences, class_ids, indexes):
        """Draw bounding boxes on the image"""
        annotated = image.copy()
        
        # Ensure we have data to draw
        if len(boxes) == 0:
            return annotated

        # Get class names from model if available, otherwise fallback might be needed but model should have them
        names = self.model.names

        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            class_id = class_ids[i]
            class_name = names[class_id]
            confidence = confidences[i]
            
            # Get color for this class
            color = self.colors.get(class_name, (0, 255, 0))
            
            # Draw rectangle
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 3)
            
            # Draw label background
            label = f"{class_name}: {confidence:.1%}"
            (label_w, label_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(annotated, (x, y - label_h - 10), (x + label_w + 5, y), color, -1)
            
            # Draw label text
            cv2.putText(annotated, label, (x + 2, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return annotated

    def image_to_base64(self, image: np.ndarray) -> str:
        """Convert OpenCV image to base64 string"""
        _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        return base64.b64encode(buffer).decode('utf-8')
