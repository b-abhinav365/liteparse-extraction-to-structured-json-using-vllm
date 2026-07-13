# Document-to-Structured-JSON

<p align="center">

AI-powered Document Intelligence Pipeline for converting unstructured documents into structured JSON using LiteParse, OCR, and Local Large Language Models.

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LiteParse](https://img.shields.io/badge/LiteParse-Document_Parser-green)
![LLM](https://img.shields.io/badge/LLM-Local-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</p>

---

# Overview

**Document-to-Structured-JSON** is an AI-powered document intelligence pipeline that transforms unstructured technical documents into structured JSON using modern document parsing and Large Language Models.

The project combines the strengths of **LiteParse** for document parsing with **local LLMs** for semantic understanding to automatically extract meaningful information from industrial manuals, engineering documents, scanned PDFs, and other technical documentation.

Unlike traditional OCR-based solutions that simply extract text, this project focuses on **understanding** document content and converting it into structured information following a predefined schema.

The current implementation specializes in **wind turbine alarm manuals**, where each alarm is automatically detected, analyzed, and converted into structured JSON that can later be used for applications such as:

- Automated form filling
- Knowledge bases
- Enterprise search
- Digital twins
- AI assistants
- RAG pipelines
- Maintenance systems

---

# Motivation

Industrial companies possess thousands of technical manuals containing valuable operational knowledge.

Unfortunately these manuals are usually stored as:

- PDF manuals
- Scanned documents
- Engineering guides
- Maintenance procedures
- Alarm documentation

Most of this information exists only as human-readable text.

Searching, organizing, and extracting this information manually is both expensive and time-consuming.

The goal of this project is to automate this entire workflow.

Instead of reading documents manually, the system automatically extracts structured information and converts it into machine-readable JSON.

---

# Problem Statement

Consider a typical industrial alarm manual.

```
Alarm Code : 5241

Description

Possible Causes

Troubleshooting Steps

Solutions

Validation
```

For a human, understanding this document is straightforward.

For a computer, however, this information is simply a collection of paragraphs.

Traditional OCR systems only extract text.

They do **not** understand:

- which text belongs to which alarm
- which paragraph represents a description
- where troubleshooting begins
- where validation ends
- relationships between sections

This project bridges that gap by combining document parsing with semantic extraction.

---

# Solution

The solution consists of two major stages.

## Stage 1 — Document Parsing

The document is parsed using **LiteParse**, which extracts:

- Native PDF text
- OCR text from images
- Reading order
- Tables
- Layout information
- Text coordinates
- Markdown representation

The result is a structured representation of the document.

---

## Stage 2 — Information Extraction

The parsed document is passed to a local Large Language Model.

The LLM understands the document context and maps the extracted information into a predefined schema.

Finally, structured JSON is generated automatically.

---

# Why LiteParse?

LiteParse is an open-source document parsing engine developed by the RunLlama team.

Unlike conventional PDF libraries that simply extract raw text, LiteParse focuses on reconstructing the semantic structure of documents.

LiteParse provides:

- Native text extraction
- OCR integration
- Layout reconstruction
- Reading order preservation
- Table extraction
- Markdown generation
- Bounding boxes
- Image extraction
- Structured page objects

This makes it particularly well suited for downstream AI applications.

---

# How LiteParse Works

When a PDF is uploaded, LiteParse performs multiple stages of processing.

```
               PDF Document
                     │
                     ▼
         Native Text Extraction
                     │
                     ▼
        Detect Images & Scanned Regions
                     │
                     ▼
                 OCR Engine
                     │
                     ▼
      Merge OCR + Native Document Text
                     │
                     ▼
          Reading Order Reconstruction
                     │
                     ▼
            Structured ParseResult
```

Instead of simply returning plain text,

LiteParse returns a structured document object containing

- complete document text
- page information
- markdown
- text positions
- layout metadata

This structured representation becomes the foundation for downstream AI processing.

---

# Project Architecture

The project extends LiteParse by introducing a schema-aware information extraction layer.

```
                    User Upload
                         │
                         ▼
                     PDF Document
                         │
                         ▼
                     LiteParse
                         │
                         ▼
              Structured ParseResult
                         │
                         ▼
               Alarm Detection Layer
                         │
                         ▼
               Prompt Construction
                         │
                         ▼
              Local Large Language Model
                         │
                         ▼
             Schema-based Information
                    Extraction
                         │
                         ▼
              Structured JSON Output
                         │
                         ▼
             Applications / Database
```

---

# End-to-End Workflow

The complete workflow implemented in this repository is illustrated below.

```
PDF
 │
 │
 ▼
LiteParse
 │
 │
 ▼
JSON
 │
 │
 ▼
Alarm Splitter
 │
 │
 ▼
Prompt Builder
 │
 │
 ▼
Local LLM
 │
 │
 ▼
Pydantic Validation
 │
 │
 ▼
Structured JSON
 │
 │
 ▼
Application
```

Every stage has a dedicated responsibility.

This modular architecture makes it easy to extend the pipeline with additional document types and schemas.

---

# Key Features

- Automated PDF parsing
- OCR support for image-based content
- Automatic alarm detection
- Schema-aware extraction
- Local LLM inference
- Multi-alarm document support
- Structured JSON generation
- Modular architecture
- Easily extensible for future document types

---

# Current Capabilities

Currently the project supports:

✅ Native PDF documents

✅ PDFs containing scanned images

✅ PDFs with OCR text

✅ Multi-page technical manuals

✅ Automatic alarm extraction

✅ Schema-based JSON generation

---

# Future Vision

The current implementation focuses on industrial alarm manuals.

However, the architecture has been intentionally designed to become a **Universal Document Intelligence Pipeline** capable of processing many different document types.

Planned support includes:

- PDF
- DOCX
- PPTX
- Excel
- Images
- CSV
- HTML

while maintaining a common structured output interface.

---

# Repository Structure

```
Document-to-Structured-JSON/

│

├── alarm_extractor/

│     ├── input/

│     ├── output/

│     ├── alarm_models.py

│     ├── alarm_splitter.py

│     ├── document_analyzer.py

│     ├── llm_converter.py

│     ├── main.py

│     ├── prompt.py

│     ├── prompt_builder.py

│     ├── schema.py

│     ├── tracking.py

│     └── requirements.txt

│

├── README.md

└── .gitignore
```

---

# Core Components

| Module | Responsibility |
|---------|----------------|
| LiteParse | Document parsing and OCR |
| Alarm Splitter | Detects and separates alarms |
| Prompt Builder | Builds LLM prompts |
| Local LLM | Semantic understanding |
| Schema | Defines structured output |
| Validator | Ensures valid JSON |
| Output Generator | Stores structured alarm JSON |

---
---

# Technology Stack

The project combines multiple technologies to build a complete Document Intelligence Pipeline.

| Technology | Purpose |
|------------|---------|
| **LiteParse** | Document parsing, OCR, layout reconstruction |
| **Python** | Core application logic |
| **Pydantic** | Schema validation |
| **Local LLM (vLLM / Ollama)** | Semantic information extraction |
| **JSON** | Structured data representation |
| **Prompt Engineering** | Schema-guided extraction |
| **Regex** | Alarm identification and splitting |

---

# Project Workflow

The pipeline consists of two independent stages.

## Stage 1 — Document Parsing

A PDF document is provided as input.

```
Wind_Manual.pdf
```

LiteParse performs several operations:

- Native text extraction
- OCR on embedded images
- Reading order reconstruction
- Layout preservation
- Markdown generation
- JSON generation

The output is a structured JSON representation of the document.

```
Wind_Manual.pdf

        │

        ▼

LiteParse

        │

        ▼

Wind_Manual.json
```

---

## Stage 2 — Alarm Information Extraction

The generated JSON is then processed by the Alarm Extraction Pipeline.

```
Wind_Manual.json

        │

        ▼

Alarm Splitter

        │

        ▼

Prompt Builder

        │

        ▼

Local LLM

        │

        ▼

Structured Alarm JSON
```

Each alarm is extracted independently and converted into a structured schema.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/<your-username>/document-to-structured-json.git
```

Navigate into the project.

```bash
cd document-to-structured-json
```

---

# Install LiteParse

LiteParse is responsible for document parsing and OCR.

Follow the official installation guide if LiteParse is not already installed.

https://github.com/run-llama/liteparse

---

# Install Project Dependencies

Navigate into the alarm extractor.

```bash
cd alarm_extractor
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file inside:

```
alarm_extractor/
```

Example:

```ini
MODEL_NAME=qwen3:35b

OLLAMA_HOST=http://localhost:11434

TEMPERATURE=0

MAX_RETRIES=3
```

If using a vLLM server instead of Ollama:

```ini
VLLM_ENDPOINT=http://localhost:8000

MODEL_NAME=qwen3:35b
```

---

# Running the Project

The workflow consists of two separate commands.

---

## Step 1 — Parse the PDF using LiteParse

Run:

```bash
lit parse pdf_name.pdf --format json -o pdf_name.json
```

Example:

```bash
lit parse wind.pdf --format json -o wind.json
```

LiteParse generates a structured JSON representation containing:

- Complete document text
- OCR text
- Page metadata
- Reading order
- Layout information

---

## Step 2 — Move JSON

Move the generated JSON into

```
alarm_extractor/input/
```

Example

```
alarm_extractor/

    input/

        wind.json
```

---

## Step 3 — Run the Alarm Extraction Pipeline

Navigate into the extractor.

```bash
cd alarm_extractor
```

Run

```bash
python main.py
```

The pipeline automatically begins processing.

---

# Internal Processing Pipeline

The execution of `main.py` consists of several stages.

```
Load JSON

      │

      ▼

Document Analysis

      │

      ▼

Alarm Detection

      │

      ▼

Alarm Splitting

      │

      ▼

Prompt Generation

      │

      ▼

Local LLM

      │

      ▼

JSON Validation

      │

      ▼

Save Output
```

---

# Module Responsibilities

## main.py

Acts as the entry point of the project.

Responsibilities:

- Load input documents
- Initialize processing pipeline
- Manage extraction workflow
- Save outputs

---

## document_analyzer.py

Responsible for:

- Reading LiteParse JSON
- Understanding document structure
- Identifying alarm regions
- Passing alarm content downstream

---

## alarm_splitter.py

Responsible for:

- Detecting alarm codes
- Separating multiple alarms
- Creating individual alarm contexts

Example:

```
5241

5242

5243
```

becomes

```
Alarm 5241

Alarm 5242

Alarm 5243
```

Each alarm is processed independently.

---

## prompt_builder.py

Constructs the prompt sent to the LLM.

The prompt contains:

- Instructions
- JSON schema
- Alarm content
- Formatting rules

This significantly improves extraction accuracy.

---

## llm_converter.py

Responsible for communicating with the Local LLM.

Tasks include:

- Sending prompts
- Receiving responses
- Parsing JSON
- Retry handling
- Error recovery

---

## schema.py

Defines the expected JSON schema using Pydantic.

Validation ensures every generated JSON follows the required format before being saved.

---

## tracking.py

Maintains a list of previously processed documents.

This prevents unnecessary reprocessing of identical inputs.

---

# Processing Example

Input

```
Alarm Code

5241

Description

Possible Causes

Troubleshooting
```

↓

Alarm Splitter

↓

```
Alarm 5241
```

↓

Prompt Builder

↓

```
Extract this alarm using the predefined schema.
```

↓

Local LLM

↓

```
{
    "alarm_code":"5241",
    "description":"...",
    ...
}
```

↓

Validation

↓

```
5241.json
```

---

# Output Directory

All generated JSON files are stored inside:

```
alarm_extractor/output/
```

Example

```
output/

5241.json

5242.json

5243.json

5244.json

wind_structured.json
```

Each alarm receives its own structured JSON representation.

---

# Current Limitations

The current version expects:

- LiteParse JSON as input
- PDF documents
- Local LLM availability
- Predefined alarm schema

Direct PDF → JSON extraction without an intermediate JSON file is planned for future releases.

---

# Performance

The modular architecture allows:

- Independent alarm extraction
- Easy model replacement
- Schema modifications
- Batch processing
- Parallel document processing

without changing the overall workflow.

---
