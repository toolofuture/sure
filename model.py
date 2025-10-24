import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import numpy as np
from typing import Tuple, Dict
from config import (
    MODEL_NAME, MODEL_PATH, PRETRAINED, NUM_CLASSES,
    IMAGE_SIZE, MEAN, STD, CONFIDENCE_THRESHOLD
)


class ArtworkVerifier:
    """ResNet-based Artwork Authenticity Verifier using Transfer Learning"""
    
    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._build_model()
        self.model.to(self.device)
        self.model.eval()
        
    def _build_model(self) -> nn.Module:
        """Build ResNet50 with transfer learning"""
        if MODEL_NAME == "resnet50":
            model = models.resnet50(pretrained=PRETRAINED)
        elif MODEL_NAME == "resnet101":
            model = models.resnet101(pretrained=PRETRAINED)
        elif MODEL_NAME == "resnet34":
            model = models.resnet34(pretrained=PRETRAINED)
        else:
            model = models.resnet50(pretrained=PRETRAINED)
        
        # Freeze backbone layers for transfer learning
        for param in model.parameters():
            param.requires_grad = False
        
        # Replace final classification layer
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, NUM_CLASSES)
        )
        
        # Unfreeze final layers for fine-tuning
        for param in model.fc.parameters():
            param.requires_grad = True
            
        return model
    
    def _preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess image to model input format"""
        # Resize
        image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to tensor
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        # Normalize
        img_tensor = torch.from_numpy(img_array).permute(2, 0, 1)
        for i, (mean, std) in enumerate(zip(MEAN, STD)):
            img_tensor[i] = (img_tensor[i] - mean) / std
        
        return img_tensor.unsqueeze(0).to(self.device)
    
    def verify(self, image: Image.Image) -> Dict[str, str]:
        """
        Verify artwork authenticity
        Returns only two results: "진품 확실" or "진품임을 확신하지 못함"
        
        Args:
            image: PIL Image object
            
        Returns:
            dict with 'result' (진품 확실 or 진품임을 확신하지 못함) 
                   and 'confidence' (신뢰도)
        """
        with torch.no_grad():
            img_tensor = self._preprocess_image(image)
            outputs = self.model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            
            # Class 0: 진품, Class 1: 불확실
            authentic_prob = probabilities[0, 0].item()
            uncertain_prob = probabilities[0, 1].item()
            
            # High confidence threshold for authenticity confirmation
            if authentic_prob >= CONFIDENCE_THRESHOLD:
                result = "진품 확실 ✅"
                confidence = f"{authentic_prob * 100:.1f}%"
                color = "green"
            else:
                result = "진품임을 확신하지 못함 ❌"
                confidence = f"{uncertain_prob * 100:.1f}%"
                color = "red"
        
        return {
            "result": result,
            "confidence": confidence,
            "color": color,
            "authentic_probability": authentic_prob,
            "uncertain_probability": uncertain_prob
        }
    
    def save_model(self, path: str = None):
        """Save model weights"""
        save_path = path or str(MODEL_PATH)
        torch.save(self.model.state_dict(), save_path)
        print(f"Model saved to {save_path}")
    
    def load_model(self, path: str = None):
        """Load model weights"""
        load_path = path or str(MODEL_PATH)
        try:
            self.model.load_state_dict(torch.load(load_path, map_location=self.device))
            print(f"Model loaded from {load_path}")
        except FileNotFoundError:
            print(f"Model not found at {load_path}. Using pretrained weights.")


def create_verifier(device: str = None) -> ArtworkVerifier:
    """Factory function to create artwork verifier instance"""
    return ArtworkVerifier(device=device)
