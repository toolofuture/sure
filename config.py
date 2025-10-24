import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent.absolute()

# Image Processing
IMAGE_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Model Thresholds
CONFIDENCE_THRESHOLD = 0.8  # 80% 이상의 신뢰도가 있을 때만 "진품 확실"

# Streamlit Configuration
STREAMLIT_THEME = "light"
STREAMLIT_LAYOUT = "centered"
