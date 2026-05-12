import numpy as np
import tensorflow as tf
import cv2
from backend.config import IMAGE_SIZE


def compute_gradcam(model, image: np.ndarray, class_idx: int = None, layer_name: str = None) -> np.ndarray:
    """Compute GradCAM heatmap for a given image and model."""
    preprocess_fn = tf.keras.applications.efficientnet_v2.preprocess_input
    input_tensor = preprocess_fn(image.astype(np.float32).copy())
    input_tensor = np.expand_dims(input_tensor, axis=0)

    # Find last conv layer
    if layer_name is None:
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4:
                layer_name = layer.name
                break
        # If model is wrapped (functional), search inside the base model
        if layer_name is None:
            for layer in model.layers:
                if hasattr(layer, "layers"):
                    for sub_layer in reversed(layer.layers):
                        if len(sub_layer.output_shape) == 4:
                            layer_name = sub_layer.name
                            break
                    if layer_name:
                        break

    if layer_name is None:
        raise ValueError("Could not find a convolutional layer in the model")

    # Build gradient model
    try:
        grad_model = tf.keras.Model(
            inputs=model.input,
            outputs=[model.get_layer(layer_name).output, model.output],
        )
    except ValueError:
        # Layer is inside a nested model
        base_model = None
        for layer in model.layers:
            if hasattr(layer, "layers"):
                base_model = layer
                break
        if base_model is None:
            raise
        conv_output = base_model.get_layer(layer_name).output
        grad_model = tf.keras.Model(
            inputs=model.input,
            outputs=[conv_output, model.output],
        )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(input_tensor)
        if class_idx is None:
            class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)
    if grads is None:
        return np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=np.float32)

    # Global average pooling of gradients
    weights = tf.reduce_mean(grads, axis=(1, 2))
    cam = tf.reduce_sum(tf.multiply(weights[:, tf.newaxis, tf.newaxis, :], conv_outputs), axis=-1)
    cam = tf.squeeze(cam).numpy()

    # ReLU and normalize
    cam = np.maximum(cam, 0)
    if cam.max() > 0:
        cam = cam / cam.max()

    # Resize to image size
    cam = cv2.resize(cam, (IMAGE_SIZE, IMAGE_SIZE))
    return cam


def generate_heatmap(cam: np.ndarray, colormap: int = cv2.COLORMAP_JET) -> np.ndarray:
    """Convert GradCAM activation map to a colored heatmap."""
    heatmap = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(heatmap, colormap)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    return heatmap


def generate_overlay(original: np.ndarray, cam: np.ndarray, alpha: float = 0.4) -> np.ndarray:
    """Blend GradCAM heatmap with original image."""
    heatmap = generate_heatmap(cam)
    if original.shape[:2] != heatmap.shape[:2]:
        heatmap = cv2.resize(heatmap, (original.shape[1], original.shape[0]))
    overlay = cv2.addWeighted(original, 1 - alpha, heatmap, alpha, 0)
    return overlay


def generate_all_visualizations(model, image: np.ndarray, class_idx: int = None) -> dict:
    """Generate all GradCAM visualizations: original, heatmap, overlay."""
    cam = compute_gradcam(model, image, class_idx)
    heatmap = generate_heatmap(cam)
    overlay = generate_overlay(image, cam)
    return {
        "original": image,
        "heatmap": heatmap,
        "overlay": overlay,
        "cam_raw": cam,
    }
