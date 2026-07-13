"""
alarm_models.py

Intermediate data models used between
LiteParse and the LLM.

Pipeline

LiteParse JSON
        │
        ▼
AlarmSplitter
        │
        ▼
AlarmSection
        │
        ▼
LLM
        │
        ▼
Structured Alarm JSON
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------
# Individual Alarm Header
# ---------------------------------------------------------

@dataclass
class AlarmHeader:
    """
    Represents one alarm code and its title.

    Example
    -------
    5241) Excess Current Phase R of Rotor
    """

    alarm_code: str
    name: str


# ---------------------------------------------------------
# Alarm Section
# ---------------------------------------------------------

@dataclass
class AlarmSection:
    """
    Represents one complete alarm block.

    One block may contain multiple alarm headers.

    Example

    Headers
    -------
    5241
    5242

    Shared Content
    --------------
    Description...

    Possible Causes...

    Troubleshooting...
    """

    headers: List[AlarmHeader] = field(default_factory=list)

    content: str = ""

    page_start: int = 0

    page_end: int = 0


# ---------------------------------------------------------
# Final Alarm
# ---------------------------------------------------------

@dataclass
class AlarmRecord:
    """
    One alarm after expansion.

    Every AlarmRecord corresponds to ONE alarm code.

    Example

    5241.json

    or

    5242.json
    """

    alarm_code: str

    name: str

    shared_content: dict = field(default_factory=dict)

    page_start: int = 0

    page_end: int = 0


# ---------------------------------------------------------
# Document Container
# ---------------------------------------------------------

@dataclass
class AlarmDocument:
    """
    Container holding all alarm sections found
    in one LiteParse document.
    """

    sections: List[AlarmSection] = field(default_factory=list)

    def __len__(self):

        return len(self.sections)

    def __iter__(self):

        return iter(self.sections)

    def append(
        self,
        section: AlarmSection,
    ):

        self.sections.append(section)