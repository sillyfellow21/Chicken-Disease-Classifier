from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import io
import json
from PIL import Image
import torch
import threading
import time

from src.pipeline import run_training_pipeline
from src.model import get_model
from src.config import load_params, get_settings
from torchvision import transforms

router = APIRouter()
training_status = {"status": "idle", "metrics": {}}

# Global model holding
current_model = None
model_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_names = ["Coccidiosis", "Healthy", "Newcastle_Disease", "Salmonella"]

def init_model():
    global current_model
    params = load_params()
    settings = get_settings()
    current_model = get_model(num_classes=params.classes)
    
    path = settings.MODEL_PATH
    import os
    if os.path.exists(path):
        current_model.load_state_dict(torch.load(path, map_location=model_device))
        print(f"Loaded trained model from {path}")
    else:
        print("No trained model found, using lightweight random weights stub.")
    
    current_model.to(model_device)
    current_model.eval()

# Helper thread for training
def training_thread():
    global training_status
    global current_model
    training_status["status"] = "running"
    training_status["metrics"] = {}
    try:
        metrics = run_training_pipeline()
        training_status["metrics"] = metrics
        
        # Reload model after training
        init_model()
        
        training_status["status"] = "success"
    except Exception as e:
        print(f"Error during training: {e}")
        training_status["status"] = f"error: {str(e)}"


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    global current_model
    if current_model is None:
        init_model()
        
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    params = load_params()
    transform = transforms.Compose([
        transforms.Resize(params.image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    input_tensor = transform(image).unsqueeze(0).to(model_device)
    
    with torch.no_grad():
        outputs = current_model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
        
    predicted_class = class_names[predicted_idx.item()]
    conf_score = confidence.item() * 100
    
    return {
        "class": predicted_class,
        "confidence": f"{conf_score:.1f}%"
    }

@router.post("/train")
async def start_training():
    global training_status
    if training_status["status"] == "running":
        return {"message": "Training is already running."}
        
    t = threading.Thread(target=training_thread)
    t.start()
    return {"message": "Training started."}

@router.get("/status")
async def get_status():
    return training_status
