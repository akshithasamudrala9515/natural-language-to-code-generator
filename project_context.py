import ast
from pathlib import Path


def summarize_python_file(file_path):
    """
    Summarize a Python file using its AST.

    Reports functions, classes, imports, and docstrings
    without executing the file.
    """

    path = Path(file_path)

    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

    except (OSError, SyntaxError, UnicodeDecodeError) as error:
        return {
            "file": str(path),
            "summary": f"Could not analyze file: {error}",
            "source": None,
        }

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            arguments = [
                argument.arg
                for argument in node.args.args
            ]

            signature = f"{node.name}({', '.join(arguments)})"

            docstring = ast.get_docstring(node) or "No docstring"

            functions.append({
                "signature": signature,
                "docstring": docstring,
            })

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

    summary_lines = [
        f"File: {path}",
        f"Functions: {len(functions)}",
        f"Classes: {', '.join(classes) or 'None'}",
        f"Imports: {', '.join(imports) or 'None'}",
    ]

    for function in functions:
        summary_lines.append(
            f"- {function['signature']}: {function['docstring']}"
        )

    return {
        "file": str(path),
        "summary": "\n".join(summary_lines),
        "source": source,
    }


def inspect_project(project_dir):
    """
    Read Python files from a project directory and
    build a context summary.
    """

    root = Path(project_dir).resolve()

    if not root.is_dir():
        raise NotADirectoryError(
            f"Project directory does not exist: {root}"
        )

    files = sorted(root.rglob("*.py"))

    project_context = []

    for file_path in files:

        # Skip generated environments and cache folders.
        if any(
            part in {
                ".git",
                ".venv",
                "venv",
                "__pycache__",
            }
            for part in file_path.parts
        ):
            continue

        relative_path = file_path.relative_to(root)

        info = summarize_python_file(file_path)

        project_context.append({
            "path": str(relative_path),
            "summary": info["summary"],
            "source": info["source"],
        })

    return project_context


def format_project_context(project_context):
    """
    Format the summaries for the LLM prompt.
    """

    sections = []

    for file_info in project_context:

        sections.append(
            f"FILE: {file_info['path']}\n"
            f"{file_info['summary']}"
        )

    return "\n\n".join(sections)