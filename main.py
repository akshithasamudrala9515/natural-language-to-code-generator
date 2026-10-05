import json
from pathlib import Path

from code_generator import (
    generate_code,
    fix_code,
    generate_project_changes,
)

from executor import execute_code

from project_context import (
    inspect_project,
    format_project_context,
)

from project_editor import apply_file_changes


PROJECT_DIR = Path("sample_project")
MAX_ATTEMPTS = 3


def run_project_tests(project_dir):
    """
    Run the sample project's test file safely.
    """

    project_dir = Path(project_dir).resolve()

    test_file = project_dir / "test_calculator.py"

    if not test_file.is_file():
        raise FileNotFoundError(
            f"Test file not found: {test_file}"
        )

    return execute_test_file(
        test_file,
        project_dir
    )


def execute_test_file(test_file, working_directory):
    """
    Execute the test file using subprocess with a timeout.
    """

    import subprocess
    import sys

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(test_file.resolve()),
            ],
            cwd=str(working_directory.resolve()),
            capture_output=True,
            text=True,
            timeout=7,
        )

        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    except subprocess.TimeoutExpired:

        return {
            "passed": False,
            "stdout": "",
            "stderr": "Tests timed out after 7 seconds.",
            "return_code": -1,
        }


def run_week2_agent(task):
    """
    Week 2: Generate, execute, observe and self-correct code.
    """

    code = generate_code(task)

    for attempt in range(1, MAX_ATTEMPTS + 1):

        print(f"\nATTEMPT {attempt}/{MAX_ATTEMPTS}")

        print("\nGenerated code:\n")
        print(code)

        result = execute_code(code)

        if result["stdout"]:
            print("\nOutput:\n")
            print(result["stdout"])

        if result["stderr"]:
            print("\nError:\n")
            print(result["stderr"])

        if result["passed"]:

            print("\nSUCCESS - CODE PASSED")

            return True

        print("\nFAILED")

        if attempt < MAX_ATTEMPTS:

            error_message = (
                result["stderr"]
                or result["stdout"]
                or "Program exited with a non-zero return code."
            )

            print(
                "\nSending error to the LLM for correction..."
            )

            code = fix_code(
                task,
                code,
                error_message,
            )

    print("\nMaximum attempts reached.")

    return False


def run_week3_agent(task):
    """
    Week 3:
    Read the project, understand the files,
    generate coordinated changes, back up files,
    apply changes and run tests.
    """

    project_dir = PROJECT_DIR.resolve()

    if not project_dir.is_dir():

        raise FileNotFoundError(
            f"Sample project not found: {project_dir}"
        )

    print("\nInspecting project files...")

    context = inspect_project(project_dir)

    if not context:

        print("No Python files found.")

        return False

    print("\nProject context:\n")

    print(
        format_project_context(context)
    )

    print(
        "\nAsking the LLM to propose coordinated edits..."
    )

    changes = generate_project_changes(
        task,
        context,
    )

    print("\nProposed files:")

    for change in changes:

        print(
            "-",
            change["path"]
        )

    # Show proposed changes
    for change in changes:

        print("\n" + "=" * 60)

        print(
            f"PROPOSED CHANGE: {change['path']}"
        )

        print("=" * 60)

        print(
            change["content"]
        )

    # Ask for approval
    approval = input(
        "\nApply these changes? Type YES to continue: "
    ).strip().upper()

    if approval != "YES":

        print("\nChanges cancelled.")

        return False

    # Apply changes and create backups
    result = apply_file_changes(
        project_dir,
        changes,
    )

    print("\nApplied files:")

    for filename in result["applied_files"]:

        print(
            "-",
            filename
        )

    print(
        "\nBackups saved in:",
        result["backup_directory"],
    )

    # Run tests
    print("\nRunning project tests...")

    test_result = run_project_tests(
        project_dir
    )

    if test_result["stdout"]:

        print("\nTest output:\n")

        print(
            test_result["stdout"]
        )

    if test_result["stderr"]:

        print("\nTest errors:\n")

        print(
            test_result["stderr"]
        )

    if test_result["passed"]:

        print(
            "\nSUCCESS - ALL TESTS PASSED"
        )

        return True

    print(
        "\nTESTS FAILED"
    )

    print(
        "\nThe changes were applied, but "
        "automatic rollback and correction "
        "are not implemented in this version."
    )

    return False


def main():

    print(
        "\n" + "=" * 60
    )

    print(
        "AI CODING AGENT - WEEK 3"
    )

    print(
        "=" * 60
    )

    print(
        "\n1. Week 2: Generate and execute code"
    )

    print(
        "2. Week 3: Understand and edit a multi-file project"
    )

    choice = input(
        "\nSelect option (1 or 2): "
    ).strip()

    task = input(
        "\nEnter your task:\n> "
    ).strip()

    if not task:

        print(
            "Task cannot be empty."
        )

        return

    try:

        if choice == "1":

            run_week2_agent(task)

        elif choice == "2":

            run_week3_agent(task)

        else:

            print(
                "Invalid option."
            )

    except (
        ValueError,
        OSError,
        json.JSONDecodeError
    ) as error:

        print(
            f"\nAgent error: {error}"
        )


if __name__ == "__main__":

    main()