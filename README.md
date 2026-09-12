# Natural Language to Code Generator

## Week 1 Project

A Python command-line tool that converts natural-language programming tasks into Python code using an LLM through the Groq API.

## Problem Statement

People who are not familiar with Python may find it difficult to convert a programming requirement written in normal English into working Python code.

This project provides a simple solution by allowing users to describe their programming task in natural language. An LLM then generates the required Python code automatically.

## Existing Solution

Normally, users need to:

- Search the internet for solutions.
- Read programming documentation.
- Write the code manually.
- Debug errors themselves.

This process can take time, especially for beginners.

## Proposed Solution

The proposed system is a Python CLI tool that:

1. Accepts a programming task in natural language.
2. Sends the task to an LLM.
3. Generates Python code.
4. Removes Markdown code fences if present.
5. Prints the generated code in the terminal.
6. Automatically saves the code to `generated_code.py`.

## Features

- Command-line interface.
- Natural-language input.
- LLM-based Python code generation.
- Uses Groq API.
- Clear system prompt.
- Removes Markdown code fences.
- Displays generated code in terminal.
- Automatically saves generated code.
- Supports string, mathematical, list, and dictionary operations.

## Technology Stack

- Python
- Groq API
- Llama 3.3
- Python-dotenv
- Git
- GitHub

## Project Structure

```text
natural-language-to-code-generator/
│
├── code_generator.py
├── requirements.txt
├── README.md
├── .gitignore
└── generated_code.py

## Requirements
Python 3.9 or higher
Internet connection
Groq API key
Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Go to the project directory:

cd natural-language-to-code-generator

Install dependencies:

pip install -r requirements.txt
API Key Setup

Create a .env file in the project directory.

Add:

GROQ_API_KEY=your_api_key_here

Do not share your API key or upload the .env file to GitHub.

How to Run

Run:

python code_generator.py

The program will ask:

Enter your task:

Enter a programming requirement such as:

Write a function to check whether a number is prime.

The generated Python code will be:

Displayed in the terminal.
Saved automatically to:
generated_code.py
System Prompt

The system prompt instructs the LLM to return only Python code.

Important instructions include:

Return ONLY Python code.
Do NOT provide explanations.
Do NOT use Markdown.
Do NOT use ``` code fences.

This allows the generated response to be saved directly as a Python file.

