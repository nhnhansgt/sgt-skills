---
name: doc-reader
description: Read and answer questions based on documents in the docs/ folder using Gemini CLI. Acts like NotebookLM but integrated into Claude Code — injects document content into Gemini context for research and analysis.
---

# Doc Reader

Document reading skill using Gemini CLI — similar to NotebookLM for Claude Code.

## Overview

The `docs/` directory contains source documents (PDF, Markdown, Text, etc.). This skill uses Gemini CLI to read these files and answer user queries.

**Key Benefits**:

- Gemini has a massive token window (1M+), capable of reading large files.
- Supports multiple formats: PDF, Markdown, Text, Code, etc.
- No need for OCR or conversion — Gemini reads PDFs directly.
- Fallback via `pdftotext` when PDFs exceed Gemini's capacity.

## Using Gemini CLI

### Verify Installation
```bash
# Check if Gemini CLI is installed
command -v gemini > /dev/null 2>&1 && echo "OK" || echo "Not installed"
```

### Document Reading Syntax

**Method 1: Read the entire docs/ directory (Recommended)**
```bash
gemini -p "@docs/ <your question>"
```

**Method 2: Read a specific file**
```bash
gemini -p "@docs/filename.pdf <your question>"
```

**Method 3: Read multiple files**
```bash
gemini -p "@docs/file1.pdf @docs/file2.md <your question>"
```

**Method 4: Pipe content (for text files)**
```bash
cat docs/file.md | gemini -p "<your question>"
```

### Important Flags

| Flag          | Description                                    |
| ------------- | ---------------------------------------------- |
| `-p "prompt"` | Run non-interactively, return results and exit |
| `--yolo`      | Automatically approve all tool calls           |
| `-m <model>`  | Select model (Default: gemini-2.5-flash)       |

### Prompt Template

When calling Gemini CLI, use the following template:
```
You are a document analysis expert. Your task is to answer questions strictly based on the provided documents.

@docs/

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

## Execution Workflow

### Step 1: Environment Check
```bash
# Check Gemini CLI
command -v gemini > /dev/null 2>&1
```

If Gemini CLI is missing → report error with installation instructions.

### Step 2: List Documents
```bash
# View file list in docs/
ls -la docs/
```

### Step 3: Call Gemini CLI
```bash
# Read all docs and answer question
gemini -p "@docs/ <prompt as per template>"
```

### Step 4: Handle Oversized PDFs (Fallback)

If Gemini CLI returns an error such as `context too long`, `token limit exceeded`, `file too large`, or similar, **do not give up**. Follow the fallback procedure below for each oversized PDF:

#### Step 4a: Check pdftotext availability
```bash
command -v pdftotext > /dev/null 2>&1 && echo "OK" || echo "Not installed"
```

If not installed:
- macOS: `brew install poppler`
- Ubuntu/Debian: `sudo apt-get install poppler-utils`
- Report to user if installation is not possible.

#### Step 4b: Convert PDF to text
```bash
# Set up auto-cleanup before starting — runs even if later steps fail
trap 'rm -f docs/largefile.txt docs/chunk_*' EXIT

# Convert a single PDF to text file
pdftotext docs/largefile.pdf docs/largefile.txt

# Preserve layout (useful for tables/columns)
pdftotext -layout docs/largefile.pdf docs/largefile.txt
```

#### Step 4c: Re-run Gemini with converted text
```bash
# Use the extracted .txt file instead of the original PDF
gemini -p "@docs/largefile.txt <prompt as per template>"
```

#### Step 4d: If still too large — chunk the text

If the extracted text file is still too large, split it into chunks and query each:
```bash
# Check line count
wc -l docs/largefile.txt

# Split into 5000-line chunks (adjust as needed)
split -l 5000 docs/largefile.txt docs/chunk_

# Query each chunk
for chunk in docs/chunk_*; do
  echo "=== $chunk ==="
  gemini -p "@$chunk <your question>"
done
```

Aggregate the results from each chunk before reporting back.

#### Step 4e: Cleanup

Remove converted and chunked files after Gemini has finished processing:
```bash
# Remove converted text file and all chunks
rm -f docs/largefile.txt
rm -f docs/chunk_*
```

> Note: If you used `trap` in Step 4b, cleanup runs automatically. This step is a manual fallback.
```

### Step 5: Report Results

Return results to the main agent in this format:
```
📄 Source: <files read>
🔧 Method: <gemini-direct | pdftotext-fallback | chunked>
---
<Answer content>
---
⚠️ Note: <any uncertainties or limitations>
```

## Decision Tree
```
Start
  │
  ▼
gemini -p "@docs/ ..."
  │
  ├─ Success ──────────────────────────────► Report results
  │
  └─ Error (token/size limit)
       │
       ▼
     pdftotext docs/file.pdf docs/file.txt
       │
       ▼
     gemini -p "@docs/file.txt ..."
       │
       ├─ Success ────────────────────►  rm -f docs/file.txt ─────────────────► Report results
       │
       └─ Still too large
              │
              ▼
            split -l 5000 → query each chunk → Aggregate
              │
              ▼
            rm -f docs/file.txt docs/chunk_* ──────────────► Report results
```

## Troubleshooting

| Error                          | Solution                                           |
| ------------------------------ | -------------------------------------------------- |
| `gemini: command not found`    | `npm install -g @google/gemini-cli`                |
| Token / context limit exceeded | Use `pdftotext` fallback (Step 4)                  |
| `pdftotext: command not found` | `brew install poppler` / `apt install poppler-utils` |
| Chunked results inconsistent   | Ask Gemini to synthesize all chunk answers at end  |
| Timeout                        | Add `--timeout 120` or split the question          |
| Images inside PDF not readable | Note limitation; text content still extracted      |

## Limitations

- **Token limit**: Gemini 2.5 Flash supports ~1M tokens, sufficient for most documents.
- **Formats**: PDF, MD, TXT, code files. Images inside PDFs might not be readable.
- **pdftotext**: Extracts text only — embedded images, charts, and complex layouts may lose fidelity.
- **Languages**: Supports multilingual analysis (Vietnamese, Japanese, English, etc.).