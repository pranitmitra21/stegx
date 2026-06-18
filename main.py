import argparse
import sys
from analyzer.core import run_analysis
from reports.generator import print_cli_report, save_json_report
from utils.encoder import encode

def main():
    parser = argparse.ArgumentParser(description="StegX - Advanced Steganography Detection Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a file for hidden data")
    analyze_parser.add_argument("-i", "--input", required=True, help="Path to the target file")
    analyze_parser.add_argument("-o", "--output", default="analysis.json", help="Path to save JSON report")
    
    encode_parser = subparsers.add_parser("encode", help="Hide a secret message (Testing Utility)")
    encode_parser.add_argument("-i", "--image", required=True, help="Path to the cover image")
    encode_parser.add_argument("-m", "--message", required=True, help="Secret text message")
    encode_parser.add_argument("-o", "--output", required=True, help="Path to save stego image")

    args = parser.parse_args()
    
    if args.command == "analyze":
        results = run_analysis(args.input)
        if results:
            print_cli_report(results)
            save_json_report(results, args.output)
        else:
            print("[-] Analysis failed or file not found.")
            sys.exit(1)
            
    elif args.command == "encode":
        try:
            encode(args.image, args.message, args.output)
        except Exception as e:
            print(f"[-] Error encoding: {e}")
            sys.exit(1)
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
