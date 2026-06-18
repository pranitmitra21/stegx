import wave
import os

def analyze_audio_lsb(file_path):
    """
    Analyzes a WAV file for LSB steganography anomalies.
    Returns (confidence, technique_name, score).
    """
    try:
        if not file_path.lower().endswith(".wav"):
             return 0, "Audio LSB", 0.0
             
        with wave.open(file_path, 'rb') as audio:
            frames = audio.readframes(10000) # Sample first 10k frames
            
            lsb_1 = 0
            lsb_0 = 0
            for byte in frames:
                if byte & 1:
                    lsb_1 += 1
                else:
                    lsb_0 += 1
                    
            if lsb_0 == 0 and lsb_1 == 0:
                return 0, "Audio LSB", 0.0
                
            ratio = min(lsb_0, lsb_1) / max(lsb_0, lsb_1)
            
            if ratio > 0.98:
                confidence = 85
            elif ratio > 0.95:
                confidence = 60
            else:
                confidence = 10
                
            return confidence, "Audio LSB", ratio
            
    except Exception as e:
        print(f"[-] Error in audio detection: {e}")
        return 0, "Audio LSB", 0.0
