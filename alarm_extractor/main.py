from pathlib import Path

from rich.console import Console

from llm_converter import AlarmConverter
from tracking import ProcessTracker

console = Console()


INPUT_FOLDER = Path("input")

OUTPUT_FOLDER = Path("output")


def main():

    console.rule("[bold blue]Alarm Extraction Pipeline[/bold blue]")

    converter = AlarmConverter()

    tracker = ProcessTracker()

    json_files = sorted(INPUT_FOLDER.glob("*.json"))

    if not json_files:

        console.print("[red]No JSON files found.[/red]")

        return

    for json_file in json_files:

        if tracker.is_processed(json_file.name):

            console.print(
                f"[yellow]Skipping {json_file.name} (already processed)[/yellow]"
            )

            continue

        console.rule(f"[green]Processing {json_file.name}[/green]")

        output_file = OUTPUT_FOLDER / f"{json_file.stem}_structured.json"

        converter.convert(

            input_json=json_file,

            output_json=output_file,

        )

        tracker.mark_processed(json_file.name)

        console.print(
            f"[green]Finished {json_file.name}[/green]"
        )

    console.rule("[bold green]All Processing Completed[/bold green]")


if __name__ == "__main__":

    main()