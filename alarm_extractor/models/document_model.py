from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path
import json

@dataclass
class Page:

    page_number: int

    text: str

    markdown: str = ""


@dataclass
class Metadata:

    source_file: str

    document_type: str

    parser: str

    page_count: int = 0

    extra: Dict = field(default_factory=dict)


@dataclass
class Document:

    metadata: Metadata

    pages: List[Page]

    def to_json(self):

        return {

            "document_type": self.metadata.document_type,

            "metadata": {

                "source_file": self.metadata.source_file,

                "parser": self.metadata.parser,

                "page_count": self.metadata.page_count,

                **self.metadata.extra,

            },

            "pages": [

                {

                    "page": page.page_number,

                    "text": page.text,

                    "markdown": page.markdown,

                }

                for page in self.pages

            ],

        }

    def save(self, output_file: str | Path):
        
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
                self.to_json(),
                f,
                indent=4,
                ensure_ascii=False,
            )