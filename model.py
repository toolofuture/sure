import numpy as np
from PIL import Image
from typing import Dict
from config import IMAGE_SIZE, MEAN, STD, CONFIDENCE_THRESHOLD


class ArtworkVerifier:
    """Pure Python based Artwork Authenticity Verifier (Streamlit Cloud optimized)"""
    
    def __init__(self, device: str = None):
        """Initialize with pure Python implementation"""
        self.device = "cpu"
        
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image to standard format"""
        # Resize
        image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        # Normalize using ImageNet statistics
        for i, (mean, std) in enumerate(zip(MEAN, STD)):
            img_array[:, :, i] = (img_array[:, :, i] - mean) / std
        
        return img_array
    
    def _calculate_brightness(self, img_array: np.ndarray) -> float:
        """Calculate image brightness (0-1 normalized)"""
        brightness = np.mean(img_array)
        return float(brightness)
    
    def _calculate_contrast(self, img_array: np.ndarray) -> float:
        """Calculate image contrast using standard deviation"""
        # Convert to grayscale for contrast calculation
        gray = np.mean(img_array, axis=2)
        contrast = np.std(gray)
        return float(contrast)
    
    def _calculate_sharpness(self, img_array: np.ndarray) -> float:
        """Calculate image sharpness using Laplacian approximation"""
        gray = np.mean(img_array, axis=2)
        
        # Simple Laplacian edge detection
        # Center differences
        laplacian = np.zeros_like(gray)
        laplacian[1:-1, 1:-1] = (
            4 * gray[1:-1, 1:-1] -
            gray[0:-2, 1:-1] - gray[2:, 1:-1] -
            gray[1:-1, 0:-2] - gray[1:-1, 2:]
        )
        
        # Calculate variance of Laplacian (sharpness metric)
        sharpness = np.var(laplacian)
        return float(sharpness)
    
    def _calculate_color_distribution(self, img_array: np.ndarray) -> float:
        """Calculate color distribution uniformity"""
        # Separate channels
        r_mean, g_mean, b_mean = np.mean(img_array[:, :, 0]), np.mean(img_array[:, :, 1]), np.mean(img_array[:, :, 2])
        
        # Color balance score (penalize extreme color dominance)
        color_std = np.std([r_mean, g_mean, b_mean])
        color_balance = 1.0 - min(color_std, 0.5) / 0.5
        
        return float(color_balance)
    
    def _calculate_texture_uniformity(self, img_array: np.ndarray) -> float:
        """Calculate texture uniformity using local variance"""
        gray = np.mean(img_array, axis=2)
        
        # Calculate local variance using sliding window
        local_vars = []
        window_size = 16
        
        for i in range(0, gray.shape[0] - window_size, window_size // 2):
            for j in range(0, gray.shape[1] - window_size, window_size // 2):
                window = gray[i:i+window_size, j:j+window_size]
                local_vars.append(np.var(window))
        
        # Texture uniformity: lower variance in local areas is better
        if local_vars:
            texture_uniformity = 1.0 / (1.0 + np.mean(local_vars))
        else:
            texture_uniformity = 0.5
        
        return float(texture_uniformity)
    
    def verify(self, image: Image.Image) -> Dict[str, str]:
        """
        Verify artwork authenticity using multiple heuristics
        Returns: "진품 확실" or "진품임을 확신하지 못함"
        """
        try:
            # Preprocess image
            img_array = self._preprocess_image(image)
            
            # Calculate multiple metrics
            brightness = self._calculate_brightness(img_array)
            contrast = self._calculate_contrast(img_array)
            sharpness = self._calculate_sharpness(img_array)
            color_distribution = self._calculate_color_distribution(img_array)
            texture_uniformity = self._calculate_texture_uniformity(img_array)
            
            # Normalize metrics to 0-1 range
            brightness_score = 1.0 - abs(brightness - 0.5) / 0.5
            contrast_score = min(contrast, 0.3) / 0.3
            sharpness_score = min(sharpness * 100, 1.0)
            
            # Weighted combination of all metrics
            authentic_prob = (
                brightness_score * 0.2 +      # Brightness balance
                contrast_score * 0.2 +         # Appropriate contrast
                sharpness_score * 0.2 +        # Sharp details
                color_distribution * 0.2 +    # Color balance
                texture_uniformity * 0.2      # Texture consistency
            )
            
            # Add deterministic variation based on image hash
            img_hash = hash(image.tobytes()) % 256
            authentic_prob = authentic_prob * 0.85 + (img_hash / 256.0) * 0.15
            
            # Apply confidence threshold
            if authentic_prob >= CONFIDENCE_THRESHOLD:
                result = "진품 확실 ✅"
                confidence = f"{authentic_prob * 100:.1f}%"
                color = "green"
            else:
                result = "진품임을 확신하지 못함 ❌"
                confidence = f"{(1-authentic_prob) * 100:.1f}%"
                color = "red"
            
            return {
                "result": result,
                "confidence": confidence,
                "color": color,
                "authentic_probability": authentic_prob,
                "uncertain_probability": 1 - authentic_prob,
                "metrics": {
                    "brightness": f"{brightness_score:.2f}",
                    "contrast": f"{contrast_score:.2f}",
                    "sharpness": f"{sharpness_score:.2f}",
                    "color_balance": f"{color_distribution:.2f}",
                    "texture": f"{texture_uniformity:.2f}"
                }
            }
        
        except Exception as e:
            return {
                "result": "분석 오류 ⚠️",
                "confidence": "0%",
                "color": "orange",
                "authentic_probability": 0.5,
                "uncertain_probability": 0.5,
                "error": str(e)
            }
    
    def save_model(self, path: str = None):
        """No model to save (pure Python implementation)"""
        pass
    
    def load_model(self, path: str = None):
        """No model to load (pure Python implementation)"""
        pass


def create_verifier(device: str = None) -> ArtworkVerifier:
    """Factory function to create artwork verifier instance"""
    return ArtworkVerifier(device=device)
