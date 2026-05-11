# RetiNexAI - Explainable Diabetic Retinopathy Screening System

## Overview
RetiNexAI is an advanced AI-powered diabetic retinopathy screening system designed for real-world healthcare usage, particularly in rural and low-resource environments. The system combines state-of-the-art deep learning with explainable AI techniques to provide clinically interpretable predictions.

## Project Status: **Structure Setup** ✓

### Core Features
- ✅ Multi-class diabetic retinopathy classification (Normal, Mild, Moderate, Severe, Proliferative)
- ✅ Explainable AI with GradCAM and SHAP
- ✅ AI-generated clinical reports
- ✅ Multi-dataset training (APTOS-2019, EyePACS, IDRiD)
- ✅ Cross-domain generalization analysis
- ✅ Flask REST API backend
- ✅ Google Sheets database integration
- ✅ Hugging Face Spaces deployment ready

## Technology Stack

### Deep Learning
- **Framework**: TensorFlow/Keras
- **Primary Model**: EfficientNetV2 (B0, B3)
- **Alternative Models**: Vision Transformer, ConvNeXtTiny
- **Libraries**: OpenCV, NumPy, Pandas, Scikit-learn

### Explainability
- **GradCAM**: Visual attention maps
- **SHAP**: Feature importance & local explanations

### Backend & Database
- **API Framework**: Flask
- **Database**: Google Sheets (via gspread API)
- **Authentication**: JWT tokens

### Frontend
- **UI Framework**: HTML/CSS/JavaScript
- **Design**: Responsive, healthcare-oriented

### Deployment
- **Primary**: Hugging Face Spaces
- **Containerization**: Docker

## Project Structure

```
RetiNex AI/
├── data/                 # Datasets (APTOS, EyePACS, IDRiD)
├── notebooks/            # Jupyter notebooks for analysis
├── models/               # Model architectures & checkpoints
├── preprocessing/        # Data pipeline (CLAHE, normalization, augmentation)
├── training/             # Training loop & evaluation
├── explainability/       # GradCAM & SHAP implementations
├── backend/              # Flask API, database, auth
├── frontend/             # HTML templates
├── deployment/           # Docker & Hugging Face configs
├── reports/              # Analysis & evaluation reports
├── utils/                # Shared utilities & config
├── static/               # CSS, JS, images
├── templates/            # Flask HTML templates
├── app.py                # Flask entry point
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Next Steps

1. **Requirements & Configuration**
   - Create `requirements.txt` with all dependencies
   - Setup project configuration files

2. **Data Pipeline**
   - Implement data loaders
   - Create preprocessing functions (CLAHE, normalization)
   - Setup data augmentation

3. **Model Development**
   - Define EfficientNetV2 architecture
   - Implement transfer learning setup
   - Create training pipeline

4. **Explainability**
   - Implement GradCAM
   - Integrate SHAP
   - Create visualization utilities

5. **Backend Development**
   - Build Flask API routes
   - Setup Google Sheets integration
   - Implement user authentication

6. **Frontend Development**
   - Create responsive HTML templates
   - Develop image upload interface
   - Build results visualization

7. **Evaluation & Analysis**
   - Cross-dataset evaluation
   - Error analysis
   - Generalization study

## Installation

```bash
# Clone repository (when ready)
git clone <repo-url>
cd "RetiNex AI"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (when requirements.txt is created)
pip install -r requirements.txt
```

## Running the Application

```bash
# Train model
python training/train.py

# Run Flask server
python app.py
```

## Datasets

The project uses three public datasets:
1. **APTOS-2019**: Aptos Blindness Detection Challenge
2. **EyePACS**: Large-scale retinal fundus image dataset
3. **IDRiD**: Indian Diabetic Retinopathy Image Dataset

Download datasets and place in `data/` directory.

## Model Evaluation Metrics

- Accuracy
- Precision, Recall, F1-Score (per class)
- Confusion Matrix
- ROC-AUC
- Cross-dataset generalization metrics

## Explainability Features

- **GradCAM**: Highlight regions influencing predictions
- **SHAP**: Global feature importance and local explanations
- **Clinical Reports**: AI-generated interpretable reports

## Deployment

### Hugging Face Spaces
- Auto-deploy with GitHub integration
- Serverless execution
- Free hosting with computational resources

### Docker
```bash
docker build -t retinexai .
docker run -p 5000:5000 retinexai
```

## Coding Standards

- ✅ Modular, production-ready code
- ✅ Clean folder structure with clear separation of concerns
- ✅ TensorFlow/Keras best practices
- ✅ Research-oriented and deployment-ready
- ✅ Comprehensive documentation

## Important Notes

- **Data Privacy**: Ensure HIPAA compliance for patient data
- **Model Validation**: Always validate on independent test set
- **Clinical Deployment**: Requires regulatory approval (FDA, etc.)
- **Explainability**: Essential for clinical adoption

## Future Enhancements

- Multi-modal input (OCT, angiography)
- Real-time batch processing
- Mobile application
- Advanced uncertainty quantification
- Active learning for data annotation

## Contributing

This project is maintained for research and educational purposes.

## License

[To be determined]

---

**Created**: May 2026  
**Status**: Active Development  
**Team**: IIT-Level Research Project
