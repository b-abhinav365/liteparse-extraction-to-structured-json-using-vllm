# """
# schema.py

# Pydantic models for validating the structured JSON returned by Ollama.
# The output of the LLM MUST conform to these models.
# """

# from typing import List
# from pydantic import BaseModel, Field, ConfigDict


# class Alarm(BaseModel):
#     """
#     Represents a single alarm extracted from the document.
#     """

#     model_config = ConfigDict(
#         extra="ignore",          # Ignore unexpected fields from the LLM
#         populate_by_name=True,
#         validate_assignment=True,
#     )

#     # -----------------------------
#     # Basic Information
#     # -----------------------------
#     alarm_code: str = Field(
#         default="",
#         description="Alarm code."
#     )

#     name: str = Field(
#         default="",
#         description="Name of the alarm."
#     )

#     description: str = Field(
#         default="",
#         description="Detailed alarm description."
#     )

#     # -----------------------------
#     # Classification
#     # -----------------------------
#     category: str = Field(
#         default="",
#         description="Alarm category."
#     )

#     alarm_group: str = Field(
#         default="",
#         description="Alarm group."
#     )

#     turbine_make: str = Field(
#         default="",
#         description="Wind turbine manufacturer."
#     )

#     turbine_model: str = Field(
#         default="",
#         description="Wind turbine model."
#     )

#     # -----------------------------
#     # Behaviour
#     # -----------------------------
#     reaction: str = Field(
#         default="",
#         description="System reaction when alarm occurs."
#     )

#     availability: str = Field(
#         default="",
#         description="Availability impact."
#     )

#     reset: str = Field(
#         default="",
#         description="Reset condition."
#     )

#     trigger_criterion: str = Field(
#         default="",
#         description="Trigger condition."
#     )

#     context_info: str = Field(
#         default="",
#         description="Additional contextual information."
#     )

#     # -----------------------------
#     # Lists
#     # -----------------------------
#     probable_causes: List[str] = Field(
#         default_factory=list,
#         description="Possible causes."
#     )

#     troubleshooting_steps: List[str] = Field(
#         default_factory=list,
#         description="Troubleshooting steps."
#     )

#     solutions: List[str] = Field(
#         default_factory=list,
#         description="Recommended solutions."
#     )

#     validation_steps: List[str] = Field(
#         default_factory=list,
#         description="Validation steps after fixing."
#     )

#     # -----------------------------
#     # Impact
#     # -----------------------------
#     impact: str = Field(
#         default="",
#         description="Business or operational impact."
#     )


# class AlarmDocument(BaseModel):
#     """
#     Root object returned by the LLM.

#     A single PDF can contain multiple alarms.
#     """

#     model_config = ConfigDict(
#         extra="ignore"
#     )

#     alarms: List[Alarm] = Field(
#         default_factory=list,
#         description="List of extracted alarms."
#     )

"""
schema.py

Universal document schema.

Every technical PDF is mapped into this schema.
"""

from typing import List, Dict

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class TechnicalDocument(BaseModel):

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        validate_assignment=True,
    )

    # =====================================================
    # DOCUMENT INFORMATION
    # =====================================================

    document_type: str = ""

    document_id: str = ""

    title: str = ""

    manufacturer: str = ""

    turbine_model: str = ""

    source_file: str = ""

    # =====================================================
    # ALARM INFORMATION
    # =====================================================

    alarm_code: str = ""

    alarm_name: str = ""

    description: str = ""

    category: str = ""

    alarm_group: str = ""

    trigger_criterion: str = ""

    reaction: str = ""

    availability: str = ""

    reset: str = ""

    context_info: str = ""

    probable_causes: List[str] = Field(default_factory=list)

    troubleshooting_steps: List[str] = Field(default_factory=list)

    solutions: List[str] = Field(default_factory=list)

    validation_steps: List[str] = Field(default_factory=list)

    impact: str = ""

    # =====================================================
    # WORK INSTRUCTION
    # =====================================================

    purpose: str = ""

    scope: str = ""

    responsibility: str = ""

    procedure: List[str] = Field(default_factory=list)

    safety_requirements: List[str] = Field(default_factory=list)

    tools: List[str] = Field(default_factory=list)

    spares: List[str] = Field(default_factory=list)

    consumables: List[str] = Field(default_factory=list)

    documents_records: List[str] = Field(default_factory=list)

    error_criteria: str = ""

    # =====================================================
    # FUTURE DOCUMENT TYPES
    # =====================================================

    extra_fields: Dict = Field(default_factory=dict)


class TechnicalDocuments(BaseModel):

    model_config = ConfigDict(
        extra="ignore"
    )

    documents: List[TechnicalDocument] = Field(
        default_factory=list
    )