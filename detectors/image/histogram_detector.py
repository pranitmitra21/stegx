import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def analyze_histogram(image_path, output_dir="output"):
    """
    Analyzes the pixel value histogram for flattening effects.
    Saves a plot and returns a confidence score.
    """
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        pixel_data = np.array(img).flatten()
        
        counts = np.bincount(pixel_data, minlength=256)
        
        diffs = []
        for i in range(0, 256, 2):
            if counts[i] > 0 or counts[i+1] > 0:
                diffs.append(abs(counts[i] - counts[i+1]) / max(counts[i], counts[i+1]))
        
        avg_diff = sum(diffs) / len(diffs) if diffs else 1.0
        if avg_diff < 0.05:
            confidence = 95
        elif avg_diff < 0.15:
            confidence = 80
        elif avg_diff < 0.3:
            confidence = 60
        else:
            confidence = 10

        plt.figure(figsize=(10, 5))
        max_val_idx = np.argmax(counts)
        start_idx = max(0, max_val_idx - 10)
        if start_idx % 2 != 0:
            start_idx -= 1
        end_idx = min(256, start_idx + 30)
        
        x = np.arange(start_idx, end_idx)
        y = counts[start_idx:end_idx]
        colors = ['blue' if i % 2 == 0 else 'orange' for i in x]
        
        plt.bar(x, y, color=colors, width=0.8)
        plt.title(f"Histogram Slice for {os.path.basename(image_path)}")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        
        os.makedirs(output_dir, exist_ok=True)
        plot_path = os.path.join(output_dir, f"histogram_{os.path.basename(image_path)}.png")
        plt.savefig(plot_path)
        plt.close()
        
        return confidence, "Histogram", plot_path
    except Exception as e:
        print(f"[-] Error in Histogram detection: {e}")
        return 0, "Histogram", None
