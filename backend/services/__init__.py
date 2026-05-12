import numpy as np
import tensorflow as tf
import cv2
import threading
from backend.config import MODEL_PATH, IMAGE_SIZE, NUM_CLASSES, CLASS_NAMES


class InferenceService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._model = None
                    cls._instance._loaded = False
        return cls._instance

    def _load_model(self):
        if self._loaded:
            return
        with self._lock:
            if not self._loaded:
                self._model = tf.keras.models.load_model(MODEL_PATH)
                self._loaded = True

    @property
    def model(self):
        self._load_model()
        return self._model

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Could not decode image")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Retinal crop
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            margin = 20
            x = max(x - margin, 0)
            y = max(y - margin, 0)
            w = min(w + 2 * margin, image.shape[1] - x)
            h = min(h + 2 * margin, image.shape[0] - y)
            image = image[y : y + h, x : x + w]

        # CLAHE enhancement
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        image = cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
        image = cv2.GaussianBlur(image, (3, 3), 0)

        # Resize with padding
        h, w, _ = image.shape
        scale = IMAGE_SIZE / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        resized = cv2.resize(image, (new_w, new_h))
        canvas = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)
        y_off = (IMAGE_SIZE - new_h) // 2
        x_off = (IMAGE_SIZE - new_w) // 2
        canvas[y_off : y_off + new_h, x_off : x_off + new_w] = resized

        return canvas

    def predict(self, image: np.ndarray) -> dict:
        preprocess_fn = tf.keras.applications.efficientnet_v2.preprocess_input
        input_tensor = preprocess_fn(image.astype(np.float32))
        input_tensor = np.expand_dims(input_tensor, axis=0)

        predictions = self.model.predict(input_tensor, verbose=0)
        probabilities = predictions[0].tolist()
        predicted_class = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_class])

        return {
            "predicted_class": predicted_class,
            "predicted_label": CLASS_NAMES[predicted_class],
            "confidence": confidence,
            "probabilities": {CLASS_NAMES[i]: round(p, 4) for i, p in enumerate(probabilities)},
            "probabilities_list": [round(p, 4) for p in probabilities],
        }

    def predict_with_tta(self, image: np.ndarray, n_augments: int = 5) -> dict:
        """Test-Time Augmentation: average predictions across augmented versions."""
        preprocess_fn = tf.keras.applications.efficientnet_v2.preprocess_input
        all_preds = []

        # Original
        inp = preprocess_fn(image.astype(np.float32).copy())
        all_preds.append(self.model.predict(np.expand_dims(inp, 0), verbose=0)[0])

        # Horizontal flip
        flipped = np.fliplr(image)
        inp = preprocess_fn(flipped.astype(np.float32).copy())
        all_preds.append(self.model.predict(np.expand_dims(inp, 0), verbose=0)[0])

        # Brightness variations
        for factor in [0.9, 1.1]:
            adjusted = np.clip(image * factor, 0, 255).astype(np.uint8)
            inp = preprocess_fn(adjusted.astype(np.float32).copy())
            all_preds.append(self.model.predict(np.expand_dims(inp, 0), verbose=0)[0])

        # Slight rotation
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), 5, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        inp = preprocess_fn(rotated.astype(np.float32).copy())
        all_preds.append(self.model.predict(np.expand_dims(inp, 0), verbose=0)[0])

        avg_preds = np.mean(all_preds, axis=0).tolist()
        predicted_class = int(np.argmax(avg_preds))
        confidence = float(avg_preds[predicted_class])

        return {
            "predicted_class": predicted_class,
            "predicted_label": CLASS_NAMES[predicted_class],
            "confidence": confidence,
            "probabilities": {CLASS_NAMES[i]: round(p, 4) for i, p in enumerate(avg_preds)},
            "probabilities_list": [round(p, 4) for p in avg_preds],
            "tta_enabled": True,
        }


inference_service = InferenceService()
