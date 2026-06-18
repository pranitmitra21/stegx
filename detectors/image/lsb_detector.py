import numpy as np
from PIL import Image

def analyze_lsb(image_path):
    """
    Performs a Chi-Square statistical attack against LSB steganography.
    Returns (confidence_score, technique_name) or None if error.
    """
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        pixel_data = np.array(img).flatten()
        counts = np.bincount(pixel_data, minlength=256)
        
        chi_square_stat = 0.0
        degrees_of_freedom = 0
        
        for i in range(0, 256, 2):
            observed_2k = counts[i]
            observed_2k_plus_1 = counts[i+1]
            expected = (observed_2k + observed_2k_plus_1) / 2.0
            
            if expected > 0:
                chi_square_stat += ((observed_2k - expected) ** 2) / expected
                chi_square_stat += ((observed_2k_plus_1 - expected) ** 2) / expected
                degrees_of_freedom += 1
                
        degrees_of_freedom -= 1
        
        if degrees_of_freedom <= 0:
            return 0, "LSB"
            
        ratio = chi_square_stat / degrees_of_freedom
        
        if ratio < 2.0:
            confidence = 99
        elif ratio < 5.0:
            confidence = 85
        elif ratio < 10.0:
            confidence = 60
        else:
            confidence = 5 # clean
            
        return confidence, "LSB"
    except Exception as e:
        print(f"[-] Error in LSB detection: {e}")
        return 0, "LSB"
