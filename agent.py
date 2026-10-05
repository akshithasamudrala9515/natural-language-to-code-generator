import argparse
import json
from pathlib import Path

from code_generator import (
    generate_project_changes,
    fix_code,
)

from project_context import (
    inspect_project,
    format_project_context,
)

from project_editor import apply_file_changes

from executor import execute_project_tests


MAX_ATTEMPTS = 3
DEFAULT_TIMEOUT = 7


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Portfolio Coding Agent"
    )

    parser.add_argument(
        "--project",
        required=True,
        help="Path to the project directory"
    )

    parser.add_argument(
        "--task",
        required=True,
        help="Natural language coding task"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show proposed changes without applying them"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Test execution timeout in seconds"
    )

    return parser.parse_args()


def run_project_tests(project_dir, timeout):
    """
    Run the existing project's tests.
    """

    return execute_project_tests(
        project_dir,
        timeout
    )

def show_project_context(project_dir):
    """
    Inspect and display the project structure.
    """

    print("\n[1/4] Inspecting project...")

    context = inspect_project(project_dir)

    if not context:
        print("No Python files found.")
        return None

    print("\nPROJECT CONTEXT")
    print("-" * 60)

    print(
        format_project_context(context)
    )

    return context


def show_proposed_changes(changes):
    """
    Display the files proposed by the LLM.
    """

    print("\nPROPOSED CHANGES")
    print("-" * 60)

    for change in changes:

        print(
            f"\nFile: {change['path']}"
        )

        print("-" * 60)

        print(
            change["content"]
        )


def apply_changes(project_dir, changes):
    """
    Apply generated changes and create backups.
    """

    print("\n[3/4] Applying changes...")

    result = apply_file_changes(
        project_dir,
        changes
    )

    print("\nApplied files:")

    for filename in result["applied_files"]:

        print(
            "-",
            filename
        )

    print(
        "\nBackups saved in:",
        result["backup_directory"]
    )

    return result


def run_tests(project_dir, timeout, attempt):
    """
    Execute project tests.
    """

    print("\n" + "=" * 60)

    print(
        f"TEST ATTEMPT {attempt}/{MAX_ATTEMPTS}"
    )

    print("=" * 60)

    result = run_project_tests(
        project_dir,
        timeout
    )

    if result["stdout"]:

        print("\nTest output:")
        print(result["stdout"])

    if result["stderr"]:

        print("\nTest errors:")
        print(result["stderr"])

    return result


def self_correct(
    task,
    project_dir,
    test_result
):
    """
    Ask the LLM to correct the project after
    a failed test run.
    """

    error_message = (
        test_result.get("stderr")
        or test_result.get("stdout")
        or "Tests failed."
    )

    print(
        "\n[AGENT] Tests failed."
    )

    print(
        "[AGENT] Sending failure information to the LLM..."
    )

    context = inspect_project(
        project_dir
    )

    formatted_context = format_project_context(
        context
    )

    fixes = fix_code(
        task,
        formatted_context,
        error_message
    )

    return fixes


def save_attempt_log(
    project_dir,
    task,
    attempts
):
    """
    Save the complete agent execution history.
    """

    logs_directory = project_dir.parent / "logs"

    logs_directory.mkdir(
        exist_ok=True
    )

    log_file = (
        logs_directory /
        "agent_attempts.json"
    )

    data = {
        "task": task,
        "attempts": attempts
    }

    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    return log_file


def run_agent(args):

    project_dir = Path(
        args.project
    ).resolve()

    if not project_dir.is_dir():

        raise FileNotFoundError(
            f"Project not found: {project_dir}"
        )

    print("\n" + "=" * 60)
    print("        PORTFOLIO CODING AGENT")
    print("=" * 60)

    print(
        f"\nProject : {project_dir}"
    )

    print(
        f"Task    : {args.task}"
    )

    print(
        f"Dry Run : {args.dry_run}"
    )

    print(
        f"Timeout : {args.timeout}s"
    )

    attempts = []

    # --------------------------------------------------
    # STEP 1 - INSPECT PROJECT
    # --------------------------------------------------

    context = show_project_context(
        project_dir
    )

    if context is None:
        return

    # --------------------------------------------------
    # STEP 2 - GENERATE CHANGES
    # --------------------------------------------------

    print(
        "\n[2/4] Analyzing task and generating changes..."
    )

    changes = generate_project_changes(
        args.task,
        context
    )

    if not changes:

        print(
            "\nNo changes were generated."
        )

        return

    show_proposed_changes(
        changes
    )

    # --------------------------------------------------
    # DRY RUN
    # --------------------------------------------------

    if args.dry_run:

        print("\n" + "=" * 60)

        print(
            "DRY RUN COMPLETE"
        )

        print(
            "No files were modified."
        )

        print("=" * 60)

        return

    # --------------------------------------------------
    # STEP 3 - APPLY CHANGES
    # --------------------------------------------------

    apply_changes(
        project_dir,
        changes
    )

    # --------------------------------------------------
    # STEP 4 - TEST + SELF CORRECT
    # --------------------------------------------------

    for attempt in range(
        1,
        MAX_ATTEMPTS + 1
    ):

        test_result = run_tests(
            project_dir,
            args.timeout,
            attempt
        )

        attempts.append(
            {
                "attempt": attempt,
                "passed": test_result["passed"],
                "stdout": test_result["stdout"],
                "stderr": test_result["stderr"]
            }
        )

        # -----------------------------
        # SUCCESS
        # -----------------------------

        if test_result["passed"]:

            print(
                "\n" + "=" * 60
            )

            print(
                "SUCCESS - ALL TESTS PASSED"
            )

            print(
                "=" * 60
            )

            log_file = save_attempt_log(
                project_dir,
                args.task,
                attempts
            )

            print(
                f"\nAttempt log saved to: {log_file}"
            )

            return

        # -----------------------------
        # MAX ATTEMPTS
        # -----------------------------

        if attempt == MAX_ATTEMPTS:

            print(
                "\n" + "=" * 60
            )

            print(
                "FAILED - MAXIMUM ATTEMPTS REACHED"
            )

            print(
                "=" * 60
            )

            break

        # -----------------------------
        # SELF CORRECTION
        # -----------------------------

        fixes = self_correct(
            args.task,
            project_dir,
            test_result
        )

        if not fixes:

            print(
                "\n[AGENT] No correction generated."
            )

            break

        print(
            "\n[AGENT] Correction generated."
        )

        show_proposed_changes(
            fixes
        )

        apply_changes(
            project_dir,
            fixes
        )

        print(
            "\n[AGENT] Correction applied."
        )

        print(
            "[AGENT] Retesting..."
        )

    save_attempt_log(
        project_dir,
        args.task,
        attempts
    )


def main():

    args = parse_arguments()

    try:

        run_agent(args)

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