import os
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
    """
    Generate Python code for a new task.
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
                "content": task
            }
        ],
        temperature=0
    )

    code = response.choices[0].message.content.strip()

    return clean_code(code)


def fix_code(task, old_code, error_message):
    """
    Ask the LLM to fix previously generated code
    based on the execution error.
    """

    prompt = f"""
The following Python code was generated for this task:

TASK:
{task}

PREVIOUS CODE:
{old_code}

The code failed during execution.

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


def clean_code(code):
    """
    Remove Markdown code fences if the model accidentally
    includes them.
    """

    if code.startswith("```python"):
        code = code[len("```python"):]

    elif code.startswith("```"):
        code = code[len("```"):]

    if code.endswith("```"):
        code = code[:-3]

    return code.strip()