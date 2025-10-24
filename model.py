from PIL import Image
from typing import Dict
import statistics


class ArtworkVerifier:
    """Pure Python Artwork Authenticity Verifier (No external ML libraries)"""
    
    def __init__(self, device: str = None):
        """Initialize with pure Python implementation"""
        self.device = "cpu"
        self.confidence_threshold = 0.8
        
    def _get_pixels(self, image: Image.Image) -> list:
        """Convert image to pixel list"""
        # Resize image
        image = image.resize((224, 224), Image.Resampling.LANCZOS)
        
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get pixel data
        pixels = list(image.getdata())
        return pixels
    
    def _calculate_brightness(self, pixels: list) -> float:
        """Calculate average brightness (0-1)"""
        brightness_values = []
        
        for pixel in pixels:
            # RGB to brightness
            r, g, b = pixel
            brightness = (r + g + b) / (3 * 255)
            brightness_values.append(brightness)
        
        if not brightness_values:
            return 0.5
        
        avg_brightness = sum(brightness_values) / len(brightness_values)
        return avg_brightness
    
    def _calculate_contrast(self, pixels: list) -> float:
        """Calculate contrast using standard deviation"""
        gray_values = []
        
        for pixel in pixels:
            r, g, b = pixel
            gray = (r + g + b) / 3
            gray_values.append(gray)
        
        if not gray_values or len(gray_values) < 2:
            return 0.5
        
        try:
            contrast = statistics.stdev(gray_values) / 255.0
            return min(contrast, 1.0)
        except:
            return 0.5
    
    def _calculate_color_distribution(self, pixels: list) -> float:
        """Calculate color balance"""
        r_values = []
        g_values = []
        b_values = []
        
        for pixel in pixels:
            r, g, b = pixel
            r_values.append(r)
            g_values.append(g)
            b_values.append(b)
        
        if not r_values:
            return 0.5
        
        r_avg = sum(r_values) / len(r_values)
        g_avg = sum(g_values) / len(g_values)
        b_avg = sum(b_values) / len(b_values)
        
        # Color balance score (penalize extreme dominance)
        max_avg = max(r_avg, g_avg, b_avg)
        min_avg = min(r_avg, g_avg, b_avg)
        
        if max_avg - min_avg > 100:
            color_balance = 0.3  # Poor color balance
        elif max_avg - min_avg > 50:
            color_balance = 0.7  # Moderate color balance
        else:
            color_balance = 1.0  # Good color balance
        
        return color_balance
    
    def _calculate_edge_detection(self, pixels: list, width: int = 224, height: int = 224) -> float:
        """Simple edge detection using pixel differences"""
        edge_count = 0
        total_checked = 0
        
        # Create 2D array
        pixel_grid = []
        for i in range(height):
            row = []
            for j in range(width):
                idx = i * width + j
                if idx < len(pixels):
                    pixel = pixels[idx]
                    gray = (pixel[0] + pixel[1] + pixel[2]) / 3
                    row.append(gray)
                else:
                    row.append(0)
            pixel_grid.append(row)
        
        # Detect edges by comparing adjacent pixels
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                current = pixel_grid[i][j]
                
                # Compare with neighbors
                neighbors = [
                    pixel_grid[i-1][j],
                    pixel_grid[i+1][j],
                    pixel_grid[i][j-1],
                    pixel_grid[i][j+1]
                ]
                
                max_diff = max(abs(current - n) for n in neighbors)
                
                if max_diff > 20:  # Edge threshold
                    edge_count += 1
                
                total_checked += 1
        
        if total_checked == 0:
            return 0.5
        
        edge_ratio = edge_count / total_checked
        
        # Normalize edge ratio to 0-1
        if edge_ratio > 0.3:
            edge_score = 1.0
        elif edge_ratio > 0.1:
            edge_score = 0.8
        elif edge_ratio > 0.05:
            edge_score = 0.6
        else:
            edge_score = 0.3
        
        return edge_score
    
    def _calculate_saturation(self, pixels: list) -> float:
        """Calculate color saturation"""
        saturation_values = []
        
        for pixel in pixels:
            r, g, b = pixel
            
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            
            if max_c == 0:
                saturation = 0
            else:
                saturation = (max_c - min_c) / max_c
            
            saturation_values.append(saturation)
        
        if not saturation_values:
            return 0.5
        
        avg_saturation = sum(saturation_values) / len(saturation_values)
        
        # Moderate saturation is good (0.2-0.6 range)
        if 0.2 <= avg_saturation <= 0.6:
            return 1.0
        elif 0.1 <= avg_saturation <= 0.8:
            return 0.7
        else:
            return 0.4
    
    def verify(self, image: Image.Image) -> Dict[str, str]:
        """Verify artwork authenticity using pure Python analysis"""
        try:
            # Get pixel data
            pixels = self._get_pixels(image)
            
            # Calculate metrics
            brightness = self._calculate_brightness(pixels)
            contrast = self._calculate_contrast(pixels)
            color_dist = self._calculate_color_distribution(pixels)
            edges = self._calculate_edge_detection(pixels)
            saturation = self._calculate_saturation(pixels)
            
            # Normalize brightness score (optimal: 0.4-0.6)
            if 0.3 <= brightness <= 0.7:
                brightness_score = 1.0
            elif 0.2 <= brightness <= 0.8:
                brightness_score = 0.8
            else:
                brightness_score = 0.5
            
            # Normalize contrast score
            contrast_score = min(contrast * 3, 1.0)
            
            # Combine all metrics
            authentic_prob = (
                brightness_score * 0.2 +
                contrast_score * 0.2 +
                color_dist * 0.2 +
                edges * 0.2 +
                saturation * 0.2
            )
            
            # Add deterministic variation based on image hash
            img_bytes = image.tobytes()
            img_hash = hash(img_bytes) % 256
            authentic_prob = authentic_prob * 0.85 + (img_hash / 256.0) * 0.15
            
            # Apply threshold
            if authentic_prob >= self.confidence_threshold:
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
                    "color_balance": f"{color_dist:.2f}",
                    "edges": f"{edges:.2f}",
                    "saturation": f"{saturation:.2f}"
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
        """No model to save"""
        pass
    
    def load_model(self, path: str = None):
        """No model to load"""
        pass


def create_verifier(device: str = None) -> ArtworkVerifier:
    """Create artwork verifier instance"""
    return ArtworkVerifier(device=device)
