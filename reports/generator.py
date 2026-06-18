import json
import os

def print_cli_report(results):
    """
    Prints a rich CLI report based on analysis results.
    """
    if not results:
        print("[-] Error: Could not analyze file.")
        return
        
    print("\n====================================")
    print("StegX v1.0")
    print("Advanced Steganography Analyzer")
    print("====================================\n")
    
    info = results["file_info"]
    print("Target File")
    print(info["file_name"])
    print("\nFile Type")
    print(info["type"])
    print("\nSize")
    print(info["size"])
    print("\nSHA256")
    print(info["sha256"])
    print("\n------------------------------------")
    print("Metadata")
    if results.get("metadata"):
        meta = results["metadata"]
        if meta["status"] == "Clean":
            print(f"[+] Clean ({meta['details']})")
        else:
            print(f"[!] {meta['status']}")
            print(f"Details: {meta['details']}")
    else:
        print("[-] No metadata analyzed")
    print("\n------------------------------------")
    print("Detection Results")
    for det in results["detections"]:
        print(f"\n{det['name']}")
        print(f"{det['confidence']}%")
        if "score" in det:
            print(f"(Raw Score: {det['score']:.4f})")
        
    print("\nOverall Confidence")
    print(f"{results['overall_confidence']}%")
    
    if results['overall_confidence'] > 60:
        print("\nLikely Steganography Detected")
        print("\n------------------------------------")
        print("Technique")
        print(results.get("technique", "Unknown"))
        
        if results.get("extraction"):
            print("\n------------------------------------")
            print("Extraction")
            print("\nPayload Found")
            print("\nType")
            print(results["extraction"]["type"])
            print("\nRecovered")
            print("Successfully")
            print("\n------------------------------------")
            print("Payload")
            safe_payload = repr(results['extraction']['data'][:100])
            print(f"{safe_payload}...")
    else:
        print("\nClean - No Steganography Detected")

    print("\n------------------------------------")
    print("Report Saved")
    print("analysis.json")
    print("====================================\n")

def save_json_report(results, output_path="analysis.json"):
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
