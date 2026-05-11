# Explainability Directory

## Purpose
Implement explainable AI techniques for model interpretability.

## Techniques
1. **GradCAM**: Gradient-weighted Class Activation Mapping
   - Visual explanations of model predictions
   - Localize disease regions
   
2. **SHAP**: SHapley Additive exPlanations
   - Feature importance analysis
   - Global and local interpretability

## Contents
- **gradcam.py**: GradCAM implementation
- **shap_explainer.py**: SHAP wrapper for medical imaging
- **visualization.py**: Heatmap and explanation visualization
- **validation.py**: Validate explanation quality

## Clinical Relevance
- Highlight affected regions (optic disc, macula, blood vessels)
- Generate physician-friendly explanations
- Error analysis through failed predictions
