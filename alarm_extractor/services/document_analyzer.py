"""
document_analyzer.py

Analyzes a LiteParse JSON document before it is sent to the LLM.

Responsibilities
----------------
1. Detect document type
2. Extract metadata
3. Extract document identifier
4. Detect section headings
5. Build a normalized document
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict
import re


# ---------------------------------------------------------
# Document Types
# ---------------------------------------------------------

class DocumentType:

    ALARM_MANUAL = "alarm_manual"

    WORK_INSTRUCTION = "work_instruction"

    TROUBLESHOOTING_GUIDE = "troubleshooting_guide"

    MAINTENANCE_MANUAL = "maintenance_manual"

    CHECKLIST = "checklist"

    UNKNOWN = "unknown"


# ---------------------------------------------------------
# Normalized Document
# ---------------------------------------------------------

@dataclass
class NormalizedDocument:

    filename: str

    document_type: str

    document_id: str

    title: str

    manufacturer: str

    turbine_model: str

    sections: Dict[str, str] = field(default_factory=dict)

    full_text: str = ""


# ---------------------------------------------------------
# Analyzer
# ---------------------------------------------------------

class DocumentAnalyzer:

    def __init__(self):

        self.section_patterns = [

            "purpose",

            "scope",

            "responsibility",

            "spares",

            "consumables",

            "tools",

            "documents",

            "records",

            "safety requirements",

            "error criteria",

            "procedure",

            "description",

            "possible causes",

            "probable causes",

            "troubleshooting",

            "solutions",

            "validation",

            "impact",

            "reaction",

            "availability",

            "reset",

            "trigger criterion",
        ]

    # -----------------------------------------------------

    def analyze(
        self,
        liteparse_json: dict,
        filename: str,
    ) -> NormalizedDocument:

        text = self.build_document(
            liteparse_json
        )

        doc_type = self.detect_document_type(text)

        document_id = self.extract_document_id(
            filename,
            text,
        )

        title = self.extract_title(
            filename,
            text,
        )

        manufacturer = self.extract_manufacturer(text)

        turbine_model = self.extract_turbine_model(text)

        sections = self.extract_sections(text)

        return NormalizedDocument(

            filename=Path(filename).name,

            document_type=doc_type,

            document_id=document_id,

            title=title,

            manufacturer=manufacturer,

            turbine_model=turbine_model,

            sections=sections,

            full_text=text,
        )

    # -----------------------------------------------------

    def build_document(
        self,
        liteparse_json: dict,
    ) -> str:

        pages = liteparse_json.get("pages", [])

        output = []

        for page in pages:

            output.append(

                page.get(
                    "text",
                    "",
                )

            )

        return "\n".join(output)

    # -----------------------------------------------------

    def detect_document_type(
        self,
        text: str,
    ) -> str:

        lower = text.lower()

        if "work instruction" in lower:

            return DocumentType.WORK_INSTRUCTION

        if "alarm" in lower:

            return DocumentType.ALARM_MANUAL

        if "troubleshooting" in lower:

            return DocumentType.TROUBLESHOOTING_GUIDE

        if "maintenance" in lower:

            return DocumentType.MAINTENANCE_MANUAL

        if "checklist" in lower:

            return DocumentType.CHECKLIST

        return DocumentType.UNKNOWN

    # -----------------------------------------------------

    def extract_document_id(
        self,
        filename: str,
        text: str,
    ) -> str:

        # Filename example:
        # WI_Error Management-208 - HU pump drive failure.pdf

        match = re.search(
            r"-(\d{2,6})",
            filename,
        )

        if match:

            return match.group(1)

        # Search inside document

        match = re.search(
            r"EM-(\d+)",
            text,
        )

        if match:

            return match.group(1)

        return ""

    # -----------------------------------------------------

    def extract_title(
        self,
        filename: str,
        text: str,
    ) -> str:

        lines = text.splitlines()

        for line in lines:

            if len(line) < 80 and line.strip():

                if "work instruction" in line.lower():

                    continue

                if "greenko" in line.lower():

                    continue

                return line.strip()

        return Path(filename).stem

    # -----------------------------------------------------

    def extract_manufacturer(
        self,
        text: str,
    ) -> str:

        lower = text.lower()

        if "gamesa" in lower:

            return "Gamesa"

        if "vestas" in lower:

            return "Vestas"

        if "ge" in lower:

            return "GE"

        if "siemens" in lower:

            return "Siemens Gamesa"

        return ""

    # -----------------------------------------------------

    def extract_turbine_model(
        self,
        text: str,
    ) -> str:

        match = re.search(

            r"(G\d+\s*&\s*G\d+)",

            text,
        )

        if match:

            return match.group(1)

        return ""

    # -----------------------------------------------------

    def extract_sections(
        self,
        text: str,
    ) -> Dict[str, str]:

        sections = {}

        current = None

        buffer = []

        lines = text.splitlines()

        for raw in lines:

            line = raw.strip()

            if not line:

                continue

            lower = line.lower()

            matched = False

            for heading in self.section_patterns:

                if heading in lower:

                    if current:

                        sections[current] = "\n".join(buffer).strip()

                    current = heading

                    buffer = []

                    matched = True

                    break

            if matched:

                continue

            if current:

                buffer.append(line)

        if current:

            sections[current] = "\n".join(buffer).strip()

        return sections