import os
import random
import string
import numpy as np
from PIL import Image
from encoder import encode

INPUT_DIR = "input_images"
OUTPUT_DIR = "test_dataset"

# For educational purposes, we simulate an encrypted payload using random characters.
# Raw English text has an ASCII bias (more 0s than 1s), which skews the perfect 50/50 
# assumption of the Chi-Square test. Real attackers encrypt before embedding.
def generate_pseudo_random_string(length):
    # We must generate characters across the full 0-255 byte range so that when 
    # converted to binary, the 0s and 1s are perfectly balanced (50/50).
    return ''.join(chr(random.randint(0, 255)) for _ in range(length))

# Varying lengths of text to test capacity and detection
SHORT_MESSAGE = "Secret"
MEDIUM_MESSAGE = generate_pseudo_random_string(10000)  # ~80,000 bits
LONG_MESSAGE = generate_pseudo_random_string(95000) # ~760,000 bits (nearly 100% capacity for a 512x512 RGB image)

def create_synthetic_image(filename, size=(512, 512)):
    """
    Creates a synthetic image with some natural-looking variance (gradients)
    so the Chi-Square test has a baseline distribution to work with.
    """
    width, height = size
    # Generate an image with gradients and some random noise
    # purely random noise would naturally trigger the detector, so we mix it
    # with a gradient to simulate a smooth photo with some texture.
    base_color = np.zeros((height, width, 3), dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            # Create a diagonal gradient
            base_color[y, x] = [(x+y) % 256, (x*2) % 256, (y*2) % 256]
            
    # Add a little uniform noise (like ISO noise in a camera)
    noise = np.random.uniform(-5, 5, (height, width, 3))
    final_image = np.clip(base_color + noise, 0, 255).astype(np.uint8)
    
    img = Image.fromarray(final_image, 'RGB')
    filepath = os.path.join(INPUT_DIR, filename)
    img.save(filepath)
    print(f"[*] Generated synthetic image: {filepath}")
    return filepath

def generate_dataset():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    input_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.bmp'))]
    
    # If no images provided, generate some synthetic ones
    if not input_files:
        print("[*] No input images found. Generating synthetic test images...")
        create_synthetic_image("test1_gradient.png")
        create_synthetic_image("test2_gradient.png")
        input_files = os.listdir(INPUT_DIR)
        
    for filename in input_files:
        base_name, ext = os.path.splitext(filename)
        input_path = os.path.join(INPUT_DIR, filename)
        
        print(f"\n--- Processing {filename} ---")
        
        # 1. Clean copy (just copy to output for comparison)
        clean_out = os.path.join(OUTPUT_DIR, f"{base_name}_clean{ext}")
        img = Image.open(input_path)
        img.save(clean_out)
        
        # 2. Short Message
        short_out = os.path.join(OUTPUT_DIR, f"{base_name}_stego_short{ext}")
        try:
            encode(input_path, SHORT_MESSAGE, short_out)
        except Exception as e:
            print(f"[-] Failed to encode short message: {e}")
            
        # 3. Medium Message
        med_out = os.path.join(OUTPUT_DIR, f"{base_name}_stego_medium{ext}")
        try:
            encode(input_path, MEDIUM_MESSAGE, med_out)
        except Exception as e:
            print(f"[-] Failed to encode medium message: {e}")
            
        # 4. Long Message
        long_out = os.path.join(OUTPUT_DIR, f"{base_name}_stego_long{ext}")
        try:
            encode(input_path, LONG_MESSAGE, long_out)
        except Exception as e:
            print(f"[-] Failed to encode long message: {e}")

if __name__ == "__main__":
    print("Generating Steganography Test Dataset...")
    generate_dataset()
    print("\n[+] Dataset generation complete. Check the 'test_dataset' directory.")
