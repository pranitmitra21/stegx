import numpy as np
from PIL import Image
import math

def analyze_entropy(image_path):
    """
    Calculates the Shannon Entropy of an image.
    High entropy (close to 8.0) indicates high randomness (encrypted/compressed data).
    Returns (confidence_score, technique_name, raw_entropy).
    """
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        pixel_data = np.array(img).flatten()
        
        counts = np.bincount(pixel_data, minlength=256)
        probabilities = counts / len(pixel_data)
        
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        
        if entropy > 7.95:
            confidence = 90
        elif entropy > 7.8:
            confidence = 75
        elif entropy > 7.5:
            confidence = 50
        else:
            confidence = 10
            
        return confidence, "Entropy", entropy
    except Exception as e:
        print(f"[-] Error in Entropy detection: {e}")
        return 0, "Entropy", 0.0
