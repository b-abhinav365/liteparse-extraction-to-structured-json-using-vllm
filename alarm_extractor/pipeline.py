"""
pipeline.py

Universal Document Processing Pipeline

Workflow
--------

                incoming/

                     │

                     ▼

            Parser Factory

          ┌────────┴────────┐

          ▼                 ▼

      PDF Parser      Excel Parser

          ▼                 ▼

             Document Model

                    ▼

             Save Raw JSON

                    ▼

          Alarm Extraction

                    ▼

        Structured JSON

                    ▼

              archive/

Author:
Abhinav
"""

from __future__ import annotations

import shutil
from pathlib import Path

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
)

from parsers.parser_factory import ParserFactory
from tracking import ProcessTracker
from llm_converter import AlarmConverter

console = Console()


class DocumentPipeline:
    """
    Main pipeline responsible for processing
    every incoming document.

    Responsibilities
    ----------------

    ✓ Scan incoming folder

    ✓ Select correct parser

    ✓ Generate raw JSON

    ✓ Generate structured JSON

    ✓ Archive processed files
    """

    def __init__(self):

        self.console = Console()

        self.tracker = ProcessTracker()

        self.converter = AlarmConverter()

        self.base_dir = Path(__file__).parent

        self.incoming_dir = self.base_dir / "incoming"

        self.input_dir = self.base_dir / "input"

        self.output_dir = self.base_dir / "output"

        self.archive_dir = self.base_dir / "archive"

        self.create_directories()

    # -----------------------------------------------------

    def create_directories(self):
        """
        Create required folders if they
        do not already exist.
        """

        for directory in [

            self.incoming_dir,

            self.input_dir,

            self.output_dir,

            self.archive_dir,

        ]:

            directory.mkdir(

                parents=True,

                exist_ok=True,

            )

    # -----------------------------------------------------

    def scan_documents(self):
        """
        Scan incoming directory.

        Returns
        -------

        List[Path]
        """

        supported = ParserFactory.supported_formats()

        documents = []

        for file in sorted(

            self.incoming_dir.iterdir()

        ):

            if (

                file.is_file()

                and file.suffix.lower()

                in supported

            ):

                documents.append(file)

        return documents

    # -----------------------------------------------------

    def generate_raw_json(
        self,
        document_path: Path,
    ) -> Path:
        """
        Convert document into the universal
        raw JSON representation.

        PDF

            ↓

        PDFParser

            ↓

        Document

            ↓

        JSON
        """

        parser = ParserFactory.get_parser(

            document_path

        )

        document = parser.parse(

            document_path

        )

        output_json = (

            self.input_dir

            / f"{document_path.stem}.json"

        )

        document.save(

            output_json

        )

        return output_json

        # -----------------------------------------------------

    def generate_structured_json(
        self,
        raw_json: Path,
    ) -> Path:
        """
        Convert raw JSON into the final
        structured JSON using the existing
        AlarmConverter.
        """

        output_json = (

            self.output_dir

            / f"{raw_json.stem}_structured.json"

        )

        self.converter.convert(

            input_json=raw_json,

            output_json=output_json,

        )

        return output_json

    # -----------------------------------------------------

    def archive_document(
        self,
        document_path: Path,
    ):
        """
        Move processed document into archive.
        """

        archive_file = (

            self.archive_dir

            / document_path.name

        )

        shutil.move(

            str(document_path),

            str(archive_file),

        )

    # -----------------------------------------------------

    def process_document(
        self,
        document_path: Path,
    ):
        """
        Complete processing for a single
        document.
        """

        if self.tracker.is_processed(

            document_path.name

        ):

            self.console.print(

                f"[yellow]Skipping[/yellow] "

                f"{document_path.name}"

            )

            return

        self.console.rule(

            f"[bold cyan]{document_path.name}[/bold cyan]"

        )

        raw_json = self.generate_raw_json(

            document_path

        )

        self.console.print(

            "[green]Raw JSON Generated[/green]"

        )

        structured_json = self.generate_structured_json(

            raw_json

        )

        self.console.print(

            "[green]Structured JSON Generated[/green]"

        )

        self.archive_document(

            document_path

        )

        self.tracker.mark_processed(

            document_path.name

        )

        self.console.print(

            f"[bold green]Completed[/bold green] "

            f"{document_path.name}"

        )

    # -----------------------------------------------------

    def run(self):
        """
        Run the complete pipeline.
        """

        documents = self.scan_documents()

        if not documents:

            self.console.print(

                "[yellow]No documents found.[/yellow]"

            )

            return

        self.console.rule(

            "[bold blue]Document Pipeline[/bold blue]"

        )

        with Progress(

            SpinnerColumn(),

            TextColumn("{task.description}"),

        ) as progress:

            task = progress.add_task(

                "Processing Documents...",

                total=None,

            )

            for document in documents:

                self.process_document(

                    document

                )

            progress.remove_task(task)

        self.console.rule(

            "[bold green]Pipeline Completed[/bold green]"


        )

# ==========================================================
# CLI
# ==========================================================

def main():

    pipeline = DocumentPipeline()

    pipeline.run()


if __name__ == "__main__":

    main()