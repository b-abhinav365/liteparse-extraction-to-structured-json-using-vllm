"""
prompt.py

Contains the system prompt and helper function for generating the final
prompt that is sent to the Ollama model.
"""

from schema import AlarmDocument


SYSTEM_PROMPT = """
You are an expert technical document parser.

Populate the following JSON schema.

If the document uses different section names,
map them to the closest matching field.

Examples:

Possible Causes → probable_causes

Root Causes → probable_causes

Alarm Description → description

Purpose → purpose

Troubleshooting → troubleshooting_steps

Procedure → procedure_steps

Safety → safety_requirements

Required Tools → tools

Leave missing fields empty.

Return ONLY JSON.
"""


def get_schema() -> dict:
    """
    Returns the Pydantic JSON schema.
    """

    return AlarmDocument.model_json_schema()


def build_prompt(document: str) -> str:
    """
    Builds the final prompt that will be sent to Ollama.
    """

    schema = get_schema()

    return f"""
{SYSTEM_PROMPT}

-------------------------------------------------------
JSON SCHEMA
-------------------------------------------------------

{schema}

-------------------------------------------------------
DOCUMENT
-------------------------------------------------------

{document}

-------------------------------------------------------
TASK
-------------------------------------------------------

Extract ALL alarms from the document.

Return ONLY JSON.

Do NOT wrap the JSON in markdown.

Return a JSON object matching the schema exactly.
"""