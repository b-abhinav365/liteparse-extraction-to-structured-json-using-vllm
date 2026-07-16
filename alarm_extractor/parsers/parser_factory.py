"""
parser_factory.py

Factory responsible for selecting the correct parser
based on the input document extension.

Supported Formats
-----------------

PDF
XLSX

Future

DOCX
PPTX
CSV
PNG
JPEG
TIFF
"""

from __future__ import annotations

from pathlib import Path

from parsers.base_parser import BaseParser
from parsers.pdf_parser import PDFParser
from parsers.excel_parser import ExcelParser


class ParserFactory:
    """
    Factory responsible for returning the correct
    parser instance.
    """

    _registry = {}

    # ---------------------------------------------------------

    @classmethod
    def register(
        cls,
        extension: str,
        parser_class,
    ):

        extension = extension.lower()

        cls._registry[extension] = parser_class

    # ---------------------------------------------------------

    @classmethod
    def get_parser(
        cls,
        document: str | Path,
    ) -> BaseParser:

        document = Path(document)

        extension = document.suffix.lower()

        parser_class = cls._registry.get(extension)

        if parser_class is None:

            supported = ", ".join(
                sorted(cls._registry.keys())
            )

            raise ValueError(
                f"Unsupported document type '{extension}'. "
                f"Supported formats: {supported}"
            )

        return parser_class()

    # ---------------------------------------------------------

    @classmethod
    def supported_formats(cls):

        return sorted(cls._registry.keys())


# ---------------------------------------------------------
# Register Parsers
# ---------------------------------------------------------

ParserFactory.register(
    ".pdf",
    PDFParser,
)

ParserFactory.register(
    ".xlsx",
    ExcelParser,
)