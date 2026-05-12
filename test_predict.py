from backend.services import inference_service
import numpy as np

try:
    print("Loading model...")
    _ = inference_service.model
    print("Model loaded successfully")
    
    img = np.zeros((299, 299, 3), dtype=np.uint8)
    res = inference_service.predict(img)
    print("Prediction:", res)
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()
