"""
llm_converter.py

Converts LiteParse JSON into a structured Alarm JSON
using a Qwen model hosted on a vLLM server.

Pipeline

LiteParse JSON
      │
      ▼
Document Builder
      │
      ▼
LLM
      │
      ▼
Pydantic Validation
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from schema import TechnicalDocument, TechnicalDocuments
from alarm_splitter import AlarmSplitter
from prompt_builder import PromptBuilder
from document_analyzer import DocumentAnalyzer
from copy import deepcopy

load_dotenv()

console = Console()


class AlarmConverter:

    """
    Converts LiteParse JSON into a structured
    alarm JSON using the company vLLM server.
    """

    def __init__(self):
        self.document_analyzer = DocumentAnalyzer()

        self.prompt_builder = PromptBuilder()
        self.base_url = os.getenv("VLLM_URL")

        self.model = os.getenv("VLLM_MODEL")

        self.api_key = os.getenv(
            "VLLM_API_KEY",
            "EMPTY"
        )

        if self.base_url is None:
            raise ValueError(
                "VLLM_URL missing in .env"
            )

        if self.model is None:
            raise ValueError(
                "VLLM_MODEL missing in .env"
            )

        console.print(
            "[green]Connecting to vLLM...[/green]"
        )

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

        console.print(
            f"[cyan]Model:[/cyan] {self.model}"
        )

    def load_liteparse_json(
        self,
        json_path: str | Path,
    ) -> dict:
        """
        Reads LiteParse JSON.
        """

        json_path = Path(json_path)

        console.print(
            f"\nReading {json_path.name}"
        )

        with open(
            json_path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def preview_document(
        self,
        document: str,
        length: int = 1500,
    ):
        """
        Prints a preview before
        sending it to the LLM.
        """

        console.print(
            "\n[bold green]Document Preview[/bold green]\n"
        )

        console.print(
            document[:length]
        )

        console.print(
            "\n..."
        )

    def get_schema(self) -> dict:
        """
        Returns the Pydantic JSON Schema.

        This becomes the single
        source of truth.
        """

        return TechnicalDocuments.model_json_schema()


    def build_system_prompt(self) -> str:
        """
        Builds the extraction instructions.

        The schema itself is NOT hardcoded.
        """

        return """
        You are an expert AI Information Extraction Engine.

        Your ONLY task is to convert the provided
        wind turbine technical documentation into
        structured JSON.

        Rules

        1. Return ONLY valid JSON.

        2. Never explain anything.

        3. Never summarize.

        4. Never invent information.

        5. If information is unavailable:

        - use "" for strings

        - use [] for arrays

        7. Extract all relevant structured information.

        8. Populate the provided JSON schema.

        9. If a field is unavailable, leave it empty.

        10. Return ONLY valid JSON.
        """

    def build_messages(
        self,
        document: str,
    ) -> list[dict[str, Any]]:
        """
        Creates the chat messages
        sent to vLLM.
        """

        schema = self.get_schema()

        user_prompt = f"""
        JSON Schema

        {json.dumps(schema, indent=2)}

        -------------------------------

        Document

        {document}

        -------------------------------

        Convert the document into the schema.

        Return ONLY JSON.
        """

        return [

            {
                "role": "system",
                "content": self.build_system_prompt(),
            },

            {
                "role": "user",
                "content": user_prompt,
            },

        ]

    def call_llm(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.0,
        max_tokens: int = 8192,
    ) -> str:
        """
        Sends the request to the vLLM server and
        returns the raw model response.
        """

        console.print("\n[cyan]Calling vLLM...[/cyan]")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if content is None:
            raise RuntimeError(
                "Model returned an empty response."
            )

        console.print("[green]Response received.[/green]")

        return content

    def parse_response(
        self,
        response_text: str,
    ) -> dict:
        """
        Converts the LLM response into Python JSON.
        """

        response_text = response_text.strip()

        # Remove markdown if the model accidentally returns it
        if response_text.startswith("```json"):
            response_text = response_text.replace(
                "```json",
                "",
                1,
            )

        if response_text.startswith("```"):
            response_text = response_text.replace(
                "```",
                "",
                1,
            )

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        try:

            parsed = json.loads(response_text)

        except Exception as e:

            console.print(
                "[red]Unable to parse model response as JSON[/red]"
            )

            console.print(response_text)

            raise e

        return parsed

    def validate(
        self,
        data: dict,
    ) -> dict:
        """
        Validate using Pydantic.
        """

        console.print(
            "\n[cyan]Validating response...[/cyan]"
        )

        validated = TechnicalDocuments.model_validate(
            data
        )

        console.print(
            "[green]Validation successful.[/green]"
        )

        return validated.model_dump()

    def extract(
        self,
        normalized_document,
    ) -> dict:

        prompt = self.prompt_builder.build_prompt(
            normalized_document
        )

        messages = [

            {
                "role": "system",
                "content": "You are an expert industrial technical document parser."
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

        raw_response = self.call_llm(
            messages
        )

        parsed = self.parse_response(
            raw_response
        )

        validated = self.validate(
            parsed
        )

        return validated

    def extract_with_retry(
        self,
        normalized_document,
        retries: int = 3,
    ) -> dict:
        """
        Executes extraction with automatic retries.

        If the model returns invalid JSON or fails validation,
        another request is sent.
        """

        last_error = None

        for attempt in range(1, retries + 1):

            console.print(
                f"\n[yellow]Attempt {attempt}/{retries}[/yellow]"
            )

            try:

                return self.extract(normalized_document)

            except Exception as e:

                last_error = e

                console.print(
                    f"[red]Attempt {attempt} failed[/red]"
                )

                console.print(str(e))

        raise RuntimeError(
            f"Extraction failed after {retries} attempts.\n{last_error}"
        )

    def save_output(
        self,
        output: dict,
        output_path: str | Path,
    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                output,
                f,
                indent=4,
                ensure_ascii=False,
            )

        console.print(
            f"[green]Saved Combined JSON[/green] -> {output_path}"
        )

        documents = output.get("documents", [])

        for document in documents:

            alarm_code = document.get(
                "alarm_code",
                "unknown"
            )

            file_path = (
                output_path.parent /
                f"{alarm_code}.json"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    document,
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

            console.print(
                f"[cyan]Saved[/cyan] {file_path.name}"
            )

    def convert(
        self,
        input_json: str | Path,
        output_json: str | Path,
    ) -> dict:
        """
        Complete extraction pipeline.

        LiteParse JSON
                ↓
        Split into Alarm Sections
                ↓
        One LLM Call per Alarm
                ↓
        Merge Results
                ↓
        Validate
                ↓
        Save JSON
        """
        liteparse_json = self.load_liteparse_json(
            input_json
        )
        normalized_doc = self.document_analyzer.analyze(
            liteparse_json=liteparse_json,
            filename=str(input_json),
        )

        console.rule("[cyan]Document Analysis[/cyan]")

        console.print(
            f"Type : {normalized_doc.document_type}"
        )

        console.print(
            f"ID   : {normalized_doc.document_id}"
        )

        console.print(
            f"Title: {normalized_doc.title}"
        )
        if normalized_doc.document_type == "alarm_manual":

            splitter = AlarmSplitter()

            alarm_sections = splitter.split(liteparse_json)

        else:

            from alarm_models import AlarmSection

            alarm_sections = [

                AlarmSection(
                    headers=[],
                    content=normalized_doc.full_text,
                )

            ]

        console.print(
            f"\n[bold green]Found {len(alarm_sections)} alarm section(s).[/bold green]"
        )

        for idx, section in enumerate(alarm_sections, start=1):

            console.rule(f"[cyan]Alarm Section {idx}[/cyan]")

            console.print("[bold yellow]Headers[/bold yellow]")

            for header in section.headers:

                console.print(
                    f"{header.alarm_code} -> {header.name}"
                )

            console.print()

            self.preview_document(
                section.content,
                length=800,
            )

        console.rule(
            "[bold green]Starting LLM Extraction[/bold green]"
        )

        all_documents = []

        for index, section in enumerate(
            alarm_sections,
            start=1,
        ):

            console.rule(
                f"[cyan]Processing Alarm Section {index}/{len(alarm_sections)}[/cyan]"
            )

            try:

                normalized_doc.full_text = section.content

                result = self.extract_with_retry(
                    normalized_document=normalized_doc
                )

                documents = result.get(
                    "documents",
                    [],
                )

                import json

                console.rule("[cyan]LLM Returned[/cyan]")

                console.print(
                    json.dumps(
                        result,
                        indent=4,
                        ensure_ascii=False,
                    )
                )

                if not documents:

                    console.print(
                        "[red]No document extracted.[/red]"
                    )

                    continue

                shared_document = documents[0]

                if normalized_doc.document_type == "work_instruction":

                    document = deepcopy(shared_document)

                    document["document_type"] = normalized_doc.document_type
                    document["document_id"] = normalized_doc.document_id
                    document["title"] = normalized_doc.title
                    document["manufacturer"] = normalized_doc.manufacturer
                    document["turbine_model"] = normalized_doc.turbine_model
                    document["source_file"] = normalized_doc.filename

                    all_documents.append(document)

                    console.print(
                        "[green]✓ Work Instruction extracted[/green]"
                    )

                    continue

                for header in section.headers:

                    document = deepcopy(shared_document)
                    document["document_type"] = normalized_doc.document_type

                    document["document_id"] = normalized_doc.document_id

                    document["title"] = (f"{header.alarm_code}) {header.name}")

                    document["manufacturer"] = normalized_doc.manufacturer

                    document["turbine_model"] = normalized_doc.turbine_model

                    document["source_file"] = normalized_doc.filename

                    document["alarm_code"] = header.alarm_code

                    document["alarm_name"] = header.name
                    document["context_info"] = (
                        f"{header.alarm_code}) {header.name}\n\n"
                        + document.get("context_info", "")
                    )

                    all_documents.append(document)

                    console.print(
                        f"[green]✓ Created Alarm {header.alarm_code}[/green]"
                    )

            except Exception as e:

                console.print(
                    f"[red]Failed Alarm Section {index}[/red]"
                )

                console.print(str(e))
        final_output = {
            "documents": all_documents
        }

        validated = TechnicalDocuments.model_validate(
            final_output
        )

        validated_json = validated.model_dump()
        self.save_output(
            validated_json,
            output_json,
        )

        console.print(
            "\n[bold green]Extraction Completed Successfully[/bold green]"
        )

        console.print(
            f"[bold cyan]Total Alarms Extracted : {len(validated_json['documents'])}[/bold cyan]"
        )

        return validated_json

    def convert_to_dict(
    self,
    input_json: str | Path,
    ) -> dict:
        """
        Processes a LiteParse JSON file and returns the
        extracted structured document as a dictionary
        without saving it.
        """
        liteparse_json = self.load_liteparse_json(
            input_json
        )
        normalized_document = self.document_analyzer.analyze(
            liteparse_json=liteparse_json,
            filename=str(input_json),
        )

        self.preview_document(
            normalized_document.full_text
        )

        result = self.extract_with_retry(
            normalized_document=normalized_document
        )

        for document in result.get("documents", []):

            document["document_type"] = normalized_document.document_type

            document["document_id"] = normalized_document.document_id

            document["title"] = normalized_document.title

            document["manufacturer"] = normalized_document.manufacturer

            document["turbine_model"] = normalized_document.turbine_model

            document["source_file"] = normalized_document.filename

        return result