from __future__ import annotations

import re

from alarm_models import (
    AlarmHeader,
    AlarmSection,
)


class AlarmSplitter:
    """
    Splits a LiteParse JSON document into logical alarm sections.

    Each section contains:

        • One or more alarm headers
        • Shared content

    Example

    5241) Rotor Phase R

    5242) Rotor Phase S

    Description...

    Possible Causes...

    Troubleshooting...

    becomes

    AlarmSection(
        headers=[5241,5242],
        content="Description..."
    )
    """

    def __init__(self):

        # Example:
        # 5241) Excess Current Phase R of Rotor

        self.header_pattern = re.compile(
            r"^(\d{4})\)\s+(.*)$"
        )

    # ---------------------------------------------------------

    def split(
        self,
        liteparse_json: dict,
    ) -> list[AlarmSection]:

        pages = liteparse_json.get(
            "pages",
            []
        )

        sections: list[AlarmSection] = []

        current_headers: list[AlarmHeader] = []

        current_content: list[str] = []

        page_start = None

        page_end = None

        inside_content = False

        # -------------------------------------------------

        for page in pages:

            page_number = page.get(
                "page",
                0
            )

            page_end = page_number

            text = page.get(
                "text",
                ""
            )

            lines = text.splitlines()

            # ---------------------------------------------

            for raw_line in lines:

                line = raw_line.strip()

                if not line:
                    continue

                match = self.header_pattern.match(
                    line
                )

                # -----------------------------------------
                # Alarm Header
                # -----------------------------------------

                if match:

                    alarm_code = match.group(1)

                    alarm_name = match.group(2).strip()

                    # New section starts only AFTER
                    # we've already entered the content
                    # of the previous alarm block.

                    if inside_content:

                        sections.append(

                            AlarmSection(

                                headers=current_headers,

                                content="\n".join(
                                    current_content
                                ),

                                page_start=page_start,

                                page_end=page_end,
                            )

                        )

                        current_headers = []

                        current_content = []

                        inside_content = False

                        page_start = page_number

                    elif page_start is None:

                        page_start = page_number

                    current_headers.append(

                        AlarmHeader(

                            alarm_code=alarm_code,

                            name=alarm_name,
                        )

                    )

                    continue

                # -----------------------------------------
                # Description starts the content
                # -----------------------------------------

                if line.lower().startswith(
                    "description"
                ):

                    inside_content = True

                if current_headers:

                    current_content.append(
                        line
                    )

        # -------------------------------------------------

        if current_headers:

            sections.append(

                AlarmSection(

                    headers=current_headers,

                    content="\n".join(
                        current_content
                    ),

                    page_start=page_start,

                    page_end=page_end,
                )

            )

        return sections

    # ---------------------------------------------------------

    def print_summary(
        self,
        sections: list[AlarmSection],
    ) -> None:

        print()

        print("=" * 80)

        print(
            f"Found {len(sections)} Alarm Sections"
        )

        print("=" * 80)

        for index, section in enumerate(
            sections,
            start=1,
        ):

            print()

            print(
                f"Alarm Block {index}"
            )

            print(
                "-" * 80
            )

            print(
                "Headers:"
            )

            for header in section.headers:

                print(
                    f"  {header.alarm_code} -> {header.name}"
                )

            print()

            print(
                f"Pages : {section.page_start} - {section.page_end}"
            )

            print()

            preview = section.content[:400]

            print(preview)

            print("...")