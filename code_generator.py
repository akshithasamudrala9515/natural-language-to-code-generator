import os
import re
from datetime import datetime

from groq import Groq
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY is not set.")
    print("Please create a .env file and add your Groq API key.")
    exit(1)


# Create Groq client
client = Groq(api_key=api_key)


# System prompt
SYSTEM_PROMPT = """
You are a Python code generator.

Your job is to convert the user's natural-language programming task
into valid, working Python code.

Rules:
1. Return ONLY Python code.
2. Do NOT provide explanations.
3. Do NOT use Markdown.
4. Do NOT use ``` code fences.
5. Write simple and readable Python code.
6. The generated code must be executable.
7. Include functions when the task asks for a function.
8. Add a small example/test at the bottom when appropriate.
"""


def clean_code(code):
    """
    Removes Markdown code fences if the LLM returns them.
    """

    code = code.strip()

    # Remove ```python and ``` fences
    code = re.sub(r"^```python\s*", "", code, flags=re.IGNORECASE)
    code = re.sub(r"^```\s*", "", code)
    code = re.sub(r"\s*```$", "", code)

    return code.strip()


def generate_code(task):
    """
    Sends the user's task to the Groq LLM and returns generated Python code.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
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
        temperature=0.2,
        max_tokens=2000
    )

    generated_code = response.choices[0].message.content

    return clean_code(generated_code)


def save_code(code):
    """
    Saves generated Python code to generated_code.py.
    """

    filename = "generated_code.py"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(code)

    return filename


def main():
    print("=" * 60)
    print("       NATURAL LANGUAGE TO CODE GENERATOR")
    print("=" * 60)

    print("\nDescribe the Python program you want to generate.")
    print("Example:")
    print("Write a function to check whether a number is prime.")

    task = input("\nEnter your task: ").strip()

    if not task:
        print("Error: Task description cannot be empty.")
        return

    print("\nGenerating Python code...")
    print("Please wait...\n")

    try:
        generated_code = generate_code(task)

        print("=" * 60)
        print("GENERATED PYTHON CODE")
        print("=" * 60)

        print(generated_code)

        filename = save_code(generated_code)

        print("\n" + "=" * 60)
        print(f"Code successfully saved to: {filename}")
        print("=" * 60)

    except Exception as error:
        print("\nError while generating code:")
        print(error)


if __name__ == "__main__":
    main()