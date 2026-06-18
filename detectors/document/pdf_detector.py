import re

def analyze_pdf(file_path):
    """
    Analyzes a PDF for common steganography vectors.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        confidence = 0
        details = []
        
        eof_index = content.rfind(b'%%EOF')
        if eof_index != -1:
            trailing_data = content[eof_index + 5:].strip()
            if len(trailing_data) > 20:
                confidence += 70
                
        if b'/JS' in content or b'/JavaScript' in content:
            confidence += 40
            
        if confidence == 0:
            confidence = 5
            
        # Instead of a complex score, return 1.0 if highly confident, else 0
        score = 1.0 if confidence > 50 else 0.0
        return min(confidence, 100), "PDF Structural Anomalies", score
    except Exception as e:
        print(f"[-] Error in PDF detection: {e}")
        return 0, "PDF Structural Anomalies", 0.0
