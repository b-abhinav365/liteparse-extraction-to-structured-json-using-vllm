"""
pdf_parser.py

PDF parser implementation using LiteParse.

Responsibilities
----------------
✓ Read PDF
✓ Parse using LiteParse
✓ Convert ParseResult -> Document Model

This class DOES NOT

✗ Save JSON
✗ Call the LLM
✗ Generate structured output
✗ Move files

Those responsibilities belong to the Pipeline.
"""

from __future__ import annotations

from pathlib import Path

from liteparse import LiteParse
from rich.console import Console

from models.document_model import (
    Document,
    Metadata,
    Page,
)

from parsers.base_parser import BaseParser


class PDFParser(BaseParser):
    """
    PDF Parser using LiteParse.
    """

    def __init__(self):

        super().__init__()

        self.console = Console()

        self.parser = LiteParse()

    # -----------------------------------------------------

    def parse(
        self,
        input_file: str | Path,
    ) -> Document:

        input_file = Path(input_file)

        self.console.rule(
            f"[bold cyan]PDF Parser[/bold cyan]"
        )

        self.console.print(
            f"[cyan]Reading[/cyan] {input_file.name}"
        )

        result = self.parser.parse(
            str(input_file)
        )

        pages = []

        for index, page in enumerate(result.pages, start=1):

            page_text = ""

            page_markdown = ""

            if hasattr(page, "text") and page.text:

                page_text = page.text

            if hasattr(page, "markdown") and page.markdown:

                page_markdown = page.markdown

            pages.append(

                Page(

                    page_number=index,

                    text=page_text,

                    markdown=page_markdown,

                )

            )

        metadata = Metadata(

            source_file=input_file.name,

            document_type="pdf",

            parser="LiteParse",

            page_count=len(pages),

        )

        document = Document(

            metadata=metadata,

            pages=pages,

        )

        self.console.print(

            f"[green]Successfully Parsed[/green] "

            f"{len(pages)} pages"

        )

        return document