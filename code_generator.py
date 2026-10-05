import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """
You are a Python code generation and debugging agent.

Generate ONLY valid Python code.

Do not use Markdown code fences.
Do not explain the code.
Do not write anything outside the Python code.

The generated program must solve the user's task.

If the user provides assertions, the generated code must satisfy all assertions.
"""


def generate_code(task):
    """Generate Python code for a new task."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": task
            }
        ],
        temperature=0
    )

    code = response.choices[0].message.content.strip()

    return clean_code(code)


def fix_code(task, old_code, error_message):
    """Fix generated code using execution feedback."""

    prompt = f"""
The following Python code was generated for this task:

TASK:
{task}

PREVIOUS CODE:
{old_code}

ERROR / OUTPUT:
{error_message}

Fix the code so that it correctly solves the task and passes
all required assertions.

Return ONLY the corrected Python code.
Do not use Markdown code fences.
Do not provide explanations.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    code = response.choices[0].message.content.strip()

    return clean_code(code)


def generate_project_changes(task, project_context):
    """
    Generate coordinated changes for multiple project files.
    """

    context_text = ""

    for file_info in project_context:
        context_text += (
            f"\n\nFILE: {file_info['path']}\n"
            f"SUMMARY:\n{file_info['summary']}\n"
            f"SOURCE CODE:\n{file_info['source']}\n"
        )

    prompt = f"""
You are an AI coding agent modifying an existing Python project.

USER REQUEST:
{task}

PROJECT CONTEXT:
{context_text}

Instructions:
1. Understand the existing project.
2. Identify all files that need changes.
3. Preserve existing functionality.
4. Return complete replacement content for each changed file.
5. Include only files that need modification.
6. Use paths relative to the project directory.
7. Modify only Python files.
8. Return valid JSON only.
9. Do not use Markdown code fences.

Return this JSON structure:

{{
    "changes": [
        {{
            "path": "calculator.py",
            "content": "complete replacement Python source"
        }},
        {{
            "path": "test_calculator.py",
            "content": "complete replacement Python source"
        }}
    ]
}}

Ensure the content fields contain complete, valid Python files.
Escape newlines and quotation marks correctly for JSON.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful Python code editor. "
                    "Return valid JSON only, with no Markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    response_text = response.choices[0].message.content.strip()

    # Remove Markdown fences if present.
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

    data = json.loads(response_text.strip())

    changes = data.get("changes")

    if not isinstance(changes, list) or not changes:
        raise ValueError("The LLM returned no project changes.")

    for change in changes:
        if not isinstance(change, dict):
            raise ValueError("Invalid change format.")

        if not isinstance(change.get("path"), str):
            raise ValueError("Missing file path.")

        if not isinstance(change.get("content"), str):
            raise ValueError("Missing file content.")

    return changes


def clean_code(code):
    """Remove Markdown code fences from generated Python code."""

    code = code.strip()

    if code.startswith("```python"):
        code = code[len("```python"):]

    elif code.startswith("```"):
        code = code[len("```"):]

    if code.endswith("```"):
        code = code[:-3]

    return code.strip()