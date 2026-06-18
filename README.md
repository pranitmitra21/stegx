# StegX - Advanced Steganography Detection & Analysis Toolkit

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-success)

**StegX** is a modular, professional-grade digital forensics toolkit designed to analyze files, detect the presence of hidden data (steganography), identify the likely hiding technique, and extract the hidden payloads. 

Originally built as a simple LSB (Least Significant Bit) detector, StegX has evolved into a multi-layered forensic pipeline capable of processing images, audio, and documents using a variety of statistical and structural heuristics.

---

## 🚀 Features

### 🔍 Multi-Format Detection Engine
*   **Images (`.png`, `.bmp`, `.jpg`)**
    *   **Chi-Square Statistical Analysis:** Detects unnatural pairing of pixel values caused by LSB embedding.
    *   **Histogram Analysis:** Visually and mathematically flags structural flattening.
    *   **Shannon Entropy:** Calculates the mathematical randomness of an image to detect highly encrypted or compressed payloads that evade traditional statistical tests.
*   **Audio (`.wav`)**
    *   **LSB Frame Analysis:** Scans raw audio frames for anomalous bit parity ratios.
*   **Documents (`.pdf`, `.docx`, `.xlsx`)**
    *   **Office ZIP Anomalies:** Tears down `.docx` XML structures to hunt for hidden executable binaries or missing manifests.
    *   **PDF Structural Anomalies:** Parses raw bytes to flag data appended after `%%EOF` markers or malicious `/JavaScript` embeddings.

### 🧬 Forensic File Triage
*   **Automatic Identification:** Automatically determines MIME types and file sizes.
*   **Cryptographic Hashing:** Generates SHA-256 hashes for all analyzed files to maintain chain-of-custody integrity.
*   **Metadata Extraction:** Extracts EXIF data and flags abnormally long hidden strings in `UserComment` or `Software` tags.

### 🛠 Automated Payload Extraction
*   If StegX achieves high confidence that a supported LSB technique was used, it will automatically attempt to carve and recover the hidden payload, presenting it safely in the terminal.

### 📊 Professional Reporting
*   Generates rich, easy-to-read CLI reports and saves the full structured output to `analysis.json`.

---

## 🏗️ Project Architecture

```text
User Input
      │
      ▼
File Identification & Hashing (hasher.py)
      │
      ▼
Dynamic Pipeline Router (analyzer/core.py)
      │
      ├──▶ Image Engine (Metadata, Entropy, LSB, Histogram)
      ├──▶ Audio Engine (WAV Frame Analysis)
      └──▶ Document Engine (PDF/DOCX Structural Analysis)
      │
      ▼
Confidence Scoring (Averages heuristics)
      │
      ▼
Payload Extraction (If applicable)
      │
      ▼
Forensic Report Generation (JSON & CLI)
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stegx.git
   cd stegx
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

The main entry point for StegX is `main.py`.

### 1. Analyze a File
To run a full forensic analysis on any supported file:
```bash
python main.py analyze -i <path_to_file>
```
*Example:* `python main.py analyze -i test_dataset/suspicious.png`

### 2. Encode a Test File (Utility)
StegX includes a utility to inject custom hidden messages into clean images so you can test the detection engines:
```bash
python main.py encode -i <clean_image.png> -m "My secret payload" -o <stego_image.png>
```

---

## 📋 Example Output

```text
====================================
StegX v1.0
Advanced Steganography Analyzer
====================================

Target File
test_stego_image.png

File Type
image/png

Size
430.20 KB

SHA256
894e270b1c1aec6a48f186cb3bfc18d4fda88fee3732baaa3a585f105aa309a2

------------------------------------
Metadata
[+] Clean (No EXIF data found.)

------------------------------------
Detection Results

LSB
99%

Histogram
95%

Entropy
90%
(Raw Score: 7.9977)

Overall Confidence
100%

Likely Steganography Detected

------------------------------------
Technique
LSB

------------------------------------
Extraction

Payload Found
Type: Text
Recovered: Successfully

------------------------------------
Payload
'This is a secret message hidden inside the image pixels...'

------------------------------------
Report Saved
analysis.json
====================================
```

---

## 🎓 Educational Disclaimer
This toolkit was developed for educational purposes, digital forensics research, and cybersecurity portfolio demonstration. Do not use this tool on files or systems you do not have explicit permission to analyze.
