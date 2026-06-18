import zipfile

def analyze_docx(file_path):
    """
    Analyzes Office Documents (DOCX/XLSX) by checking internal ZIP structure.
    """
    try:
        if not zipfile.is_zipfile(file_path):
            return 0, "Office ZIP Anomalies", 0.0
            
        confidence = 0
        
        with zipfile.ZipFile(file_path, 'r') as z:
            file_list = z.namelist()
            
            suspicious_files = []
            for name in file_list:
                if name.endswith('.exe') or name.endswith('.bin') or name.startswith('.'):
                    suspicious_files.append(name)
                    
            if suspicious_files:
                confidence += 80
                
            if '[Content_Types].xml' not in file_list:
                confidence += 50
                
        if confidence == 0:
            confidence = 5
            
        score = 1.0 if confidence > 50 else 0.0
        return min(confidence, 100), "Office ZIP Anomalies", score
    except Exception as e:
        print(f"[-] Error in DOCX detection: {e}")
        return 0, "Office ZIP Anomalies", 0.0
