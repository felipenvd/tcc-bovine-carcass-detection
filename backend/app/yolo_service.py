import cv2
import numpy as np
import os
import base64

class YoloService:
    def __init__(self):
        # Paths to model files - now in backend/models/
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
        self.config_path = os.path.join(self.base_path, "deteccao-carcacas-bovinas.cfg")
        self.weights_path = os.path.join(self.base_path, "deteccao-carcacas-bovinas_best.weights")
        self.names_path = os.path.join(self.base_path, "deteccao-carcacas-bovinas.names")
        
        # Load class names
        with open(self.names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        # Colors for each class (BGR format)
        self.colors = {
            'Lesao': (0, 0, 255),    # Red
            'Perda': (255, 165, 0),  # Orange
        }
            
        print(f"Loading YOLO from {self.config_path} and {self.weights_path}...")
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        # Get output layers
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def predict(self, image: np.ndarray):
        height, width = image.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.3:  # Threshold
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Non-max suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        results = []
        if len(indexes) > 0:
            for i in indexes.flatten():
                results.append({
                    "class": self.classes[class_ids[i]],
                    "confidence": float(confidences[i]),
                    "box": boxes[i]
                })
                
        return results, boxes, confidences, class_ids, indexes

    def draw_detections(self, image: np.ndarray, boxes, confidences, class_ids, indexes):
        """Draw bounding boxes on the image"""
        annotated = image.copy()
        
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                class_name = self.classes[class_ids[i]]
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
