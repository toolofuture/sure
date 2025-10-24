import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent.absolute()
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Model Configuration
MODEL_NAME = "resnet50"
MODEL_PATH = MODELS_DIR / "resnet50_artwork_verifier.pt"
PRETRAINED = True
NUM_CLASSES = 2  # 진품 확실(0), 진품임을 확신하지 못함(1)

# Image Processing
IMAGE_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Model Thresholds
CONFIDENCE_THRESHOLD = 0.8  # 80% 이상의 신뢰도가 있을 때만 "진품 확실"
UNCERTAIN_THRESHOLD = 0.5   # 50% 미만이면 "불확실"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_OPENAI_ANALYSIS = False  # Optional: Use OpenAI for additional analysis

# Streamlit Configuration
STREAMLIT_THEME = "light"
STREAMLIT_LAYOUT = "centered"
