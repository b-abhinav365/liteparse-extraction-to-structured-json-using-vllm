"""
base_parser.py

Abstract base class for all document parsers.

Every parser (PDF, Excel, Word, Image, etc.)
must inherit from this class and return a
Document object.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from rich.console import Console

from models.document_model import Document


class BaseParser(ABC):
    """
    Base class for all document parsers.

    Every parser must implement parse()
    and return a Document object.
    """

    def __init__(self):

        self.console = Console()

    @abstractmethod
    def parse(
        self,
        input_file: str | Path,
    ) -> Document:
        """
        Parse a document.

        Parameters
        ----------
        input_file : str | Path

        Returns
        -------
        Document
            Universal document model.
        """
        pass
    # ---------------------------------------------------------
    # Shared Utility Methods
    # ---------------------------------------------------------

    def save_json(
        self,
        document: Document,
        output_file: str | Path,
    ) -> Path:
        """
        Save a Document as JSON.
        """

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                document.to_json(),
                f,
                indent=4,
                ensure_ascii=False,
            )

        self.console.print(
            f"[green]Saved[/green] {output_file.name}"
        )

        return output_file

    # ---------------------------------------------------------

    def create_output_path(
        self,
        input_file: str | Path,
        output_directory: str | Path,
    ) -> Path:
        """
        Create an output JSON path.

        Example

        wind.pdf

            ↓

        input/

            ↓

        wind.json
        """

        input_file = Path(input_file)

        output_directory = Path(output_directory)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return output_directory / f"{input_file.stem}.json"

    # ---------------------------------------------------------

    def convert(
        self,
        input_file: str | Path,
        output_directory: str | Path,
    ) -> Path:
        """
        Complete conversion pipeline.

        Document
            ↓
        Parser
            ↓
        Document Model
            ↓
        JSON
        """

        self.console.rule(
            f"[bold cyan]{self.__class__.__name__}[/bold cyan]"
        )

        document = self.parse(
            input_file
        )

        output_json = self.create_output_path(
            input_file,
            output_directory,
        )

        self.save_json(
            document,
            output_json,
        )

        return output_json