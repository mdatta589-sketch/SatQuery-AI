from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch

# This assumes `model` and `processor` are already loaded globally in your Kaggle notebook!
# Example:
# model = PaliGemmaForConditionalGeneration.from_pretrained("google/paligemma-3b-ft-rsvqa-hr-224").to("cuda:0")
# processor = AutoProcessor.from_pretrained("google/paligemma-3b-ft-rsvqa-hr-224")

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "ok", 
        "model": "google/paligemma-3b-ft-rsvqa-hr-224",
        "grounding_model": "GroundingDINO_SwinT_OGC"
    }

@app.post("/vqa")
async def vqa_endpoint(
    image: UploadFile = File(...),
    question: str = Form(...),
    image_id: str = Form(None),
    modality: str = Form(None),
    representation: str = Form(None)
):
    try:
        # Read and prepare the image
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Prepare inputs for PaliGemma
        inputs = processor(text=question, images=pil_image, return_tensors="pt").to(model.device)
        
        # Execute Inference
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_new_tokens=50)
            
        # Decode the answer
        # PaliGemma appends the answer after the input tokens
        input_len = inputs["input_ids"].shape[-1]
        answer = processor.decode(generated_ids[0][input_len:], skip_special_tokens=True).strip()
        
        return {
            "status": "success",
            "model": "google/paligemma-3b-ft-rsvqa-hr-224",
            "answer": answer
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Return generic 500 without HTML stacktrace
        return JSONResponse(status_code=500, content={
            "status": "error",
            "model": "google/paligemma-3b-ft-rsvqa-hr-224",
            "error": "Internal inference error occurred. Check Kaggle logs."
        })

@app.post("/ground")
async def ground_endpoint(
    image: UploadFile = File(...),
    text: str = Form(...),
    box_threshold: float = Form(0.3),
    text_threshold: float = Form(0.25),
    image_id: str = Form(None),
    modality: str = Form("optical"),
    representation: str = Form("true-color")
):
    try:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        if grounding_model == "mock_grounding_model":
            boxes = torch.tensor([[0.5, 0.5, 0.1, 0.1]])
            logits = torch.tensor([0.9])
            phrases = ["road"]
        else:
            # Using standard GroundingDINO transforms assuming groundingdino is installed
            import groundingdino.datasets.transforms as T
            from groundingdino.util.inference import predict
            
            transform = T.Compose([
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])
            image_tensor, _ = transform(pil_image, None)
            
            # Execute Inference (assumes grounding_model is loaded globally)
            boxes, logits, phrases = predict(
                model=grounding_model,
                image=image_tensor,
                caption=text,
                box_threshold=box_threshold,
                text_threshold=text_threshold
            )
        
        w, h = pil_image.size
        detections = []
        for box, logit, phrase in zip(boxes, logits, phrases):
            cx, cy, bw, bh = box.tolist()
            x1 = (cx - bw/2) * w
            y1 = (cy - bh/2) * h
            x2 = (cx + bw/2) * w
            y2 = (cy + bh/2) * h
            detections.append({
                "box": [x1, y1, x2, y2],
                "score": float(logit),
                "phrase": phrase
            })
            
        return {
            "status": "success",
            "model": "GroundingDINO_SwinT_OGC",
            "image_id": image_id,
            "modality": modality,
            "representation": representation,
            "detections": detections
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={
            "status": "error",
            "model": "GroundingDINO_SwinT_OGC",
            "error": f"Internal inference error: {str(e)}"
        })

# --- Kaggle Notebook Server Management ---
import uvicorn
import threading
import time
import sys
import asyncio

# Mock models for local testing if not on Kaggle
if "model" not in globals():
    class MockModel:
        device = "cpu"
        def generate(self, **kwargs):
            return [[0, 1, 2]]
    model = MockModel()

if "processor" not in globals():
    class MockProcessor:
        def __call__(self, **kwargs):
            return {"input_ids": torch.tensor([[0]])}
        def decode(self, *args, **kwargs):
            return "mock answer"
    processor = MockProcessor()

if "grounding_model" not in globals():
    grounding_model = "mock_grounding_model"

# Robust server runner
global _kaggle_server
global _kaggle_thread

def run_server():
    global _kaggle_server, _kaggle_thread
    
    # If a server is already running in this session, shut it down cleanly
    if '_kaggle_server' in globals() and _kaggle_server is not None:
        print("Stopping existing Uvicorn server...")
        _kaggle_server.should_exit = True
        if '_kaggle_thread' in globals() and _kaggle_thread is not None:
            _kaggle_thread.join(timeout=5)
        print("Existing server stopped.")
        time.sleep(1)

    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    _kaggle_server = uvicorn.Server(config)
    
    _kaggle_thread = threading.Thread(target=_kaggle_server.run, daemon=True)
    _kaggle_thread.start()
    
    # Wait a moment for it to start
    time.sleep(2)
    print("New Uvicorn server started on port 8000.")

if __name__ == "__main__":
    run_server()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
