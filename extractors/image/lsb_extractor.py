import numpy as np
from PIL import Image
from utils.constants import DELIMITER

def extract_lsb_message(image_path):
    """
    Extracts a hidden message from an image encoded with LSB steganography.
    Returns the message string or None if no message found.
    """
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        pixel_data = np.array(img)
        flat_data = pixel_data.flatten()
        
        binary_message = ""
        current_text = ""
        for value in flat_data:
            binary_message += str(value & 1)
            
            if len(binary_message) == 8:
                char = chr(int(binary_message, 2))
                current_text += char
                binary_message = "" 
                
                if current_text.endswith(DELIMITER):
                    return {"type": "Text", "data": current_text[:-len(DELIMITER)]}
                    
        return None
    except Exception as e:
        print(f"[-] Error extracting LSB: {e}")
        return None
