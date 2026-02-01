# NotebookLM Integration Guide

This guide explains how to use Google NotebookLM with the TSTR.directory project.

## 1. Generate the Context File

Run the following command from the project root to generate a single concentrated documentation file:

```bash
python3 management/generate_notebooklm_context.py
```

This will create a file named `TSTR_CONTEXT_FOR_NOTEBOOKLM.md` in the project root.

## 2. Upload to NotebookLM

1. Go to [NotebookLM](https://notebooklm.google.com/).
2. Create a new Notebook named "TSTR.directory Project".
3. Click "Add source".
4. Upload the generated `TSTR_CONTEXT_FOR_NOTEBOOKLM.md` file.

## 3. Recommended Queries

Once uploaded, you can ask questions like:

- "What is the current architecture of TSTR.directory?"
- "What are the P0 priorities for the project?"
- "How do the scrapers currently handle authentication?"
- "Summarize the recent work on the contact page."
- "What are the common troubleshooting steps for OCI scrapers?"

## 4. Keeping it Updated

Whenever you make significant changes to the documentation or architecture, re-run the script and re-upload the file (or replace the old version) in NotebookLM to keep its knowledge fresh.
