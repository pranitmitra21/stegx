from PIL import Image
from PIL.ExifTags import TAGS

def analyze_metadata(image_path):
    """
    Extracts EXIF metadata using Pillow and checks for suspicious fields.
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if not exif_data:
            return {"status": "Clean", "details": "No EXIF data found."}
            
        parsed_exif = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            parsed_exif[tag_name] = value
            
        suspicious_tags = ["UserComment", "Software", "ImageDescription"]
        found_suspicious = []
        
        for tag in suspicious_tags:
            if tag in parsed_exif:
                # If there's a long comment, it might be a payload
                val = str(parsed_exif[tag])
                if len(val) > 50:
                    found_suspicious.append(f"Long {tag} ({len(val)} chars)")
                    
        if found_suspicious:
            return {
                "status": "Suspicious", 
                "details": f"Suspicious fields found: {', '.join(found_suspicious)}",
                "raw": parsed_exif
            }
            
        return {"status": "Clean", "details": "Standard EXIF data present."}
    except AttributeError:
        # Image does not have _getexif method (e.g., PNG)
        return {"status": "Clean", "details": "Format does not support standard EXIF."}
    except Exception as e:
        print(f"[-] Error reading metadata: {e}")
        return {"status": "Unknown", "details": "Error parsing metadata."}
