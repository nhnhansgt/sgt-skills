# Doc Reader Skill

Skill for reading and answering questions based on specified documents or directories using Gemini CLI. Acts like NotebookLM but integrated directly into Claude Code — injecting document content into Gemini's context for research and analysis.

## Overview

The provided target directory or file contains source documents (PDF, Markdown, Text, etc.). This skill uses Gemini CLI to read these files directly to answer user questions or queries.

**Key Benefits**:

- Massive token window (1M+ tokens) of Gemini, allowing it to read entire large documents or codebases.
- Supports various formats: PDF, Markdown, Text, Code, etc.
- No complex OCR or format conversion needed — Gemini reads PDFs directly.
- Strong fallback mechanism via `pdftotext` for PDF files exceeding model limits.

## Usage Guide

### 1. Environment Check

Ensure Gemini CLI is installed and configured:

```bash
command -v gemini > /dev/null 2>&1 && echo "OK" || echo "Not installed"
```

### 2. Document Reading Syntax

**Method 1: Read an entire directory (Recommended)**

```bash
gemini -p "@<path-to-directory>/ <your question>"
```

**Method 2: Read a specific file**

```bash
gemini -p "@<path-to-file.pdf> <your question>"
```

**Method 3: Read multiple files**

```bash
gemini -p "@<path-to-file1.pdf> @<path-to-file2.md> <your question>"
```

**Method 4: Pipe content (for text files)**

```bash
cat <path-to-file.md> | gemini -p "<your question>"
```

### 3. Standard Prompt Template (Input for Gemini)

Use the following prompt framework for high accuracy (replace `@<target-path>` with the actual file/directory path):

```text
You are a document analysis expert. Your task is to answer questions strictly based on the provided documents.

@<target-path>

---

Question: <user question>

Instructions:
- Answer in the SAME LANGUAGE as the question above.
- Base your answer ONLY on the document content above. Do NOT use outside knowledge.
- Cite the source file name (and page number if available) for every key claim.
- If multiple documents contain relevant information, synthesize them and note any conflicts.
- If the documents do NOT contain enough information to answer, say so explicitly — do not guess.
- Keep the answer concise and structured. Use bullet points or sections where appropriate.
```

## Large Document Fallback Mechanism

If errors like `context too long`, `token limit exceeded`, or `file too large` occur, do not stop; instead, apply these fallback steps:

1. **Recover with `pdftotext`**
   - Ensure you have `poppler` (Mac) or `poppler-utils` (Ubuntu/Devian).
   - Convert PDF to plain text:
     ```bash
     pdftotext <path>/largefile.pdf <path>/largefile.txt
     ```
     _(Optional: add `-layout` to preserve table/column formatting)_

2. **Run via Gemini with new `.txt` file**
   - Query Gemini with the extracted data:
     ```bash
     gemini -p "@<path>/largefile.txt <prompt>"
     ```

3. **Chunking for still oversized `.txt` files**
   - Check line count and split the original file (e.g., 5000 lines/file):
     ```bash
     split -l 5000 <path>/largefile.txt <path>/chunk_
     ```
   - Iterate through each chunk, send to Gemini, and then aggregate the results.

4. **Cleanup**
   - Always remember to clean up temporary files:
     ```bash
     rm -f <path>/largefile.txt <path>/chunk_*
     ```

## Result Return Structure

Analysis results for the documents must be returned according to this standard:

```text
📄 Source: <Files read>
🔧 Method: <gemini-direct | pdftotext-fallback | chunked>
---
<Answer content>
---
⚠️ Note: <Limitations or uncertainties if documents are unclear/missing (if any)>
```

## Troubleshooting

| Error / Issue                     | Solution                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------- |
| `gemini: command not found`       | Run `npm install -g @google/gemini-cli`                                       |
| Token context limit exceeded      | Use `pdftotext` fallback mechanism to extract text                            |
| `pdftotext: command not found`    | `brew install poppler` (MacOS) or `apt install poppler-utils`                 |
| Chunking results are inconsistent | Ask Gemini to analyze and synthesize all chunk results at the end             |
| Processing timeout                | Add timeout parameter like `--timeout 120` or split the prompt                |
| Image content unreadable          | Accept this limitation and note that text within images couldn't be retrieved |
