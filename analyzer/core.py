from hashes.hasher import identify_file
from detectors.image.lsb_detector import analyze_lsb
from detectors.image.histogram_detector import analyze_histogram
from detectors.image.entropy_detector import analyze_entropy
from extractors.image.lsb_extractor import extract_lsb_message
from metadata.image_metadata import analyze_metadata
from detectors.audio.lsb_detector import analyze_audio_lsb
from detectors.document.pdf_detector import analyze_pdf
from detectors.document.docx_detector import analyze_docx

def run_analysis(file_path):
    """
    Runs the full analysis pipeline on a given file.
    """
    results = {
        "target_file": file_path,
        "file_info": None,
        "metadata": None,
        "detections": [],
        "overall_confidence": 0,
        "technique": None,
        "extraction": None
    }
    
    # 1. File Identification
    file_info = identify_file(file_path)
    if not file_info:
        return None
    results["file_info"] = file_info
    
    file_type = file_info["type"].lower()
    
    if "image" in file_type:
        # 1.5 Metadata Analysis
        results["metadata"] = analyze_metadata(file_path)
        
        # 2. Steganography Detection Engine
        lsb_conf, _ = analyze_lsb(file_path)
        results["detections"].append({"name": "LSB", "confidence": lsb_conf})
        
        hist_conf, _, hist_plot = analyze_histogram(file_path)
        results["detections"].append({"name": "Histogram", "confidence": hist_conf, "plot": hist_plot})
        
        ent_conf, _, ent_score = analyze_entropy(file_path)
        results["detections"].append({"name": "Entropy", "confidence": ent_conf, "score": ent_score})
        
        avg_conf = (lsb_conf + hist_conf + ent_conf) / 3
        
        # 3. Payload Extraction Attempt
        extracted = extract_lsb_message(file_path)
        
        if extracted:
            results["overall_confidence"] = 100
            results["technique"] = "LSB"
            results["extraction"] = extracted
        else:
            results["overall_confidence"] = int(avg_conf)
            if avg_conf > 60:
                results["technique"] = "Unknown Steganography (No Payload Recovered)"
                
    elif "audio" in file_type or file_path.endswith(".wav"):
        audio_conf, name, score = analyze_audio_lsb(file_path)
        results["detections"].append({"name": name, "confidence": audio_conf, "score": score})
        results["overall_confidence"] = int(audio_conf)
        if audio_conf > 60:
            results["technique"] = "Audio LSB"
            
    elif "pdf" in file_type or file_path.endswith(".pdf"):
        pdf_conf, name, score = analyze_pdf(file_path)
        results["detections"].append({"name": name, "confidence": pdf_conf, "score": score})
        results["overall_confidence"] = int(pdf_conf)
        if pdf_conf > 60:
            results["technique"] = "PDF Append/JS"
            
    elif "word" in file_type or "zip" in file_type or file_path.endswith(".docx") or file_path.endswith(".xlsx"):
        docx_conf, name, score = analyze_docx(file_path)
        results["detections"].append({"name": name, "confidence": docx_conf, "score": score})
        results["overall_confidence"] = int(docx_conf)
        if docx_conf > 60:
            results["technique"] = "Office Zip Anomalies"
                
    return results
