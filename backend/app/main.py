from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import uvicorn
from contextlib import asynccontextmanager
from .yolo_service import YoloService

yolo_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global yolo_service
    yolo_service = YoloService()
    yield

app = FastAPI(title="TCC - Detecção de Carcaças", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API de Detecção de Carcaças Bovinas Online"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Get predictions and raw data for drawing
    results, boxes, confidences, class_ids, indexes = yolo_service.predict(img)
    
    # Draw detections on image
    annotated_img = yolo_service.draw_detections(img, boxes, confidences, class_ids, indexes)
    
    # Convert annotated image to base64
    annotated_base64 = yolo_service.image_to_base64(annotated_img)
    
    # Determine overall status
    has_lesao = any(r['class'] == 'Lesao' for r in results)
    has_perda = any(r['class'] == 'Perda' for r in results)
    
    status = "Normal"
    if has_lesao and has_perda:
        status = "Crítico (Lesão e Perda)"
    elif has_lesao:
        status = "Atenção (Lesão Detectada)"
    elif has_perda:
        status = "Perda Identificada"
        
    return {
        "filename": file.filename,
        "detections": results,
        "summary": status,
        "annotated_image": f"data:image/jpeg;base64,{annotated_base64}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
