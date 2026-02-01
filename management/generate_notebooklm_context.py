import os
import datetime

# Configuration
FILES_TO_INCLUDE = [
    "TSTR.md",
    "PROJECT_STATUS.md",
    "GEMINI.md",
    "START_HERE.md",
    ".ai-session.md",
    "web/tstr-frontend/package.json",
    "web/tstr-automation/requirements.txt"
]

OUTPUT_FILE = "TSTR_CONTEXT_FOR_NOTEBOOKLM.md"

def generate_context():
    root_dir = os.getcwd()
    print(f"Generating NotebookLM context from {root_dir}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("# TSTR.directory Project Context for NotebookLM\n")
        outfile.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        outfile.write("This file contains the core documentation and configuration for the TSTR.directory project. "
                      "It is intended to be uploaded as a source for Google NotebookLM.\n\n")
        
        for filepath in FILES_TO_INCLUDE:
            full_path = os.path.join(root_dir, filepath)
            if os.path.exists(full_path):
                print(f"Adding {filepath}...")
                outfile.write(f"\n--- BEGIN FILE: {filepath} ---\n\n")
                try:
                    with open(full_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error reading file: {str(e)}\n")
                outfile.write(f"\n\n--- END FILE: {filepath} ---\n\n")
            else:
                print(f"Warning: {filepath} not found.")
                outfile.write(f"\n--- FILE NOT FOUND: {filepath} ---\n\n")

    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_context()
