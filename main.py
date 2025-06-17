import argparse
import json
import os
from legal_analyzer import analyze_legal_document, display_analysis
from web_app import app

def process_file_cli(file_path, output_path=None):
    """Process a file using command line interface"""
    try:
        # Analyze document
        results = analyze_legal_document(file_path)
        
        # Display results
        display_analysis(results)
        
        # Save results if output file specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {output_path}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Legal Document Analysis and Summarization Tool"
    )
    parser.add_argument(
        "--mode",
        choices=['web', 'cli'],
        default='web',
        help="Run mode: 'web' for web interface, 'cli' for command line interface"
    )
    parser.add_argument(
        "--file",
        help="Path to the legal document to analyze (required for CLI mode)"
    )
    parser.add_argument(
        "--output",
        help="Output file path for saving results (optional for CLI mode)"
    )
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        if not args.file:
            print("Error: --file argument is required in CLI mode")
            parser.print_help()
            return
        process_file_cli(args.file, args.output)
    else:
        # Create uploads directory if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        # Run web application
        print("Starting web server...")
        print("Open http://localhost:5000 in your web browser")
        app.run(debug=True)

if __name__ == "__main__":
    main() 