"""
prompt_builder.py

Builds a prompt dynamically based on
the document type detected by the
DocumentAnalyzer.
"""

from __future__ import annotations

import json

from schema import TechnicalDocuments


class PromptBuilder:

    def __init__(self):

        self.schema = TechnicalDocuments.model_json_schema()

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------
    # --------------------------------------------------
# Common Rules
# --------------------------------------------------

    def common_rules(self) -> str:

        return """
    ==============================
    GENERAL EXTRACTION RULES
    ==============================

    You are an expert industrial technical document parser.

    Your task is to extract information exactly as it appears in the document.

    GENERAL RULES

    1. Return ONLY valid JSON.

    2. Do NOT return Markdown.

    3. Do NOT return explanations.

    4. Do NOT invent information.

    5. If a field is missing,
    leave it empty.

    6. Preserve the original wording
    whenever possible.

    7. Preserve the hierarchy of
    procedures and troubleshooting
    steps.

    8. Keep bullet points belonging
    to the same step together.

    9. If different section names
    represent the same meaning,
    map them to the correct schema field.

    10. If a section does not fit
        any schema field,
        store it inside:

        extra_fields

    11. Never create new keys that
        are not part of the JSON template.

    12. Never modify values that
        already exist in the document.

    13. Return ONLY the JSON object.
    """


    def build_prompt(
        self,
        normalized_document,
    ) -> str:

        document_type = normalized_document.document_type

        if document_type == "alarm_manual":

            return self.build_alarm_prompt(
                normalized_document
            )

        elif document_type == "work_instruction":

            return self.build_work_instruction_prompt(
                normalized_document
            )

        return self.build_generic_prompt(
            normalized_document
        )

    # --------------------------------------------------
    # Alarm Prompt
    # --------------------------------------------------

    def build_alarm_prompt(
        self,
        document,
    ) -> str:

        rules = self.common_rules()

        return f"""
    {rules}

    ==============================
    DOCUMENT TYPE
    ==============================

    Wind Turbine Alarm Manual

    The metadata below is already known and MUST NOT be generated:

    - document_type
    - document_id
    - title
    - manufacturer
    - turbine_model
    - source_file
    - alarm_code
    - alarm_name

    Your task is ONLY to extract the semantic content.

    ==============================
    SECTION MAPPING
    ==============================

    Map semantically equivalent headings to the same schema field.

    Description
    Alarm Description
    Overview
    Problem Description
    → description

    Possible Causes
    Root Causes
    Reasons
    Cause Analysis
    → probable_causes

    Trigger
    Alarm Trigger
    Error Criteria
    Trigger Condition
    → trigger_criterion

    Troubleshooting
    Troubleshooting Guide
    Diagnostic Procedure
    Repair Procedure
    Diagnostic Steps
    → troubleshooting_steps

    Corrective Action
    Corrective Actions
    Recommended Action
    Solution
    Repair
    → solutions

    Validation
    Verification
    Testing
    Checks
    → validation_steps

    Impact
    Effect
    Result
    → impact

    ==============================
    OUTPUT JSON
    ==============================

    {{
        "documents":[
            {{
                "description":"",
                "category":"",
                "alarm_group":"",
                "trigger_criterion":"",
                "reaction":"",
                "availability":"",
                "reset":"",
                "context_info":"",
                "probable_causes":[],
                "troubleshooting_steps":[],
                "solutions":[],
                "validation_steps":[],
                "impact":"",
                "purpose":"",
                "scope":"",
                "responsibility":"",
                "procedure":[],
                "safety_requirements":[],
                "tools":[],
                "spares":[],
                "consumables":[],
                "documents_records":[],
                "error_criteria":"",
                "extra_fields":{{}}
            }}
        ]
    }}

    ==============================
    DOCUMENT
    ==============================

    {document.full_text}
    """

    # --------------------------------------------------
    # Work Instruction Prompt
    # --------------------------------------------------

    def build_work_instruction_prompt(
        self,
        document,
    ) -> str:

        rules = self.common_rules()

        return f"""
    {rules}

    ==============================
    DOCUMENT TYPE
    ==============================

    Work Instruction

    The metadata below is already known and MUST NOT be generated:

    - document_type
    - document_id
    - title
    - manufacturer
    - turbine_model
    - source_file

    Your task is ONLY to extract the semantic content.

    ==============================
    SECTION MAPPING
    ==============================

    Map semantically equivalent headings.

    Purpose
    Objective
    Introduction
    → purpose

    Scope
    Application
    Applicability
    → scope

    Responsibility
    Responsibilities
    Owner
    → responsibility

    Procedure
    Method
    Steps
    Instructions
    Work Steps
    → procedure

    Required Tools
    Tools Required
    Equipment
    → tools

    Spare Parts
    Spares
    Replacement Parts
    → spares

    Consumables
    Materials
    → consumables

    Documents
    References
    Records
    Documents & Records
    → documents_records

    Safety
    Warnings
    Precautions
    Safety Requirements
    → safety_requirements

    Error Criteria
    Acceptance Criteria
    Inspection Criteria
    → error_criteria

    Description
    Overview
    Summary
    → description

    ==============================
    OUTPUT JSON
    ==============================

    {{
        "documents":[
            {{
                "purpose":"",
                "scope":"",
                "responsibility":"",
                "description":"",
                "procedure":[],
                "tools":[],
                "spares":[],
                "consumables":[],
                "documents_records":[],
                "safety_requirements":[],
                "error_criteria":"",
                "extra_fields":{{}}
            }}
        ]
    }}

    ==============================
    DOCUMENT
    ==============================

    {document.full_text}
    """

    # --------------------------------------------------
    # Generic Prompt
    # --------------------------------------------------

    def build_generic_prompt(
        self,
        document,
    ) -> str:

            return f"""
    You are an expert technical document parser.

    Determine the important information
    inside the document.

    Populate as many fields of the schema
    as possible.

    If information is unavailable,
    leave it blank.

    Return JSON matching:

    {json.dumps(self.schema, indent=2)}

    DOCUMENT

    {document.full_text}

    Return ONLY JSON.
    """