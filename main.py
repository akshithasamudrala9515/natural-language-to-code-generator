from code_generator import generate_code, fix_code
from executor import execute_code
from datetime import datetime


MAX_ATTEMPTS = 3


def log_attempt(attempt_number, code, result, log_file="agent_log.txt"):
    """
    Save details of every execution attempt.
    """

    with open(log_file, "a", encoding="utf-8") as file:

        file.write("\n")
        file.write("=" * 70 + "\n")
        file.write(
            f"ATTEMPT {attempt_number} - "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        file.write("=" * 70 + "\n")

        file.write("\n--- GENERATED CODE ---\n")
        file.write(code)

        file.write("\n\n--- STDOUT ---\n")
        file.write(result["stdout"] or "(no output)")

        file.write("\n\n--- STDERR ---\n")
        file.write(result["stderr"] or "(no error)")

        file.write("\n\n--- RETURN CODE ---\n")
        file.write(str(result["return_code"]))

        file.write("\n\n--- STATUS ---\n")
        file.write("PASSED\n" if result["passed"] else "FAILED\n")


def run_agent(task):

    print("\n" + "=" * 70)
    print("NATURAL LANGUAGE TO CODE - SELF-CORRECTING AGENT")
    print("=" * 70)

    print("\nTask:")
    print(task)

    print("\nGenerating initial code...")

    code = generate_code(task)

    # --------------------------------------------------
    # DEMO MODE
    # --------------------------------------------------
    # Set this to True only when recording the
    # self-correction demonstration.
    #
    # It intentionally makes Attempt 1 fail.
    # The error is then sent to the LLM for correction.
    # --------------------------------------------------

    demo_mode = True

    if demo_mode:
        code = code + '\nassert False, "Demo failure: please fix the code"'

    # --------------------------------------------------

    for attempt in range(1, MAX_ATTEMPTS + 1):

        print("\n" + "-" * 70)
        print(f"ATTEMPT {attempt}/{MAX_ATTEMPTS}")
        print("-" * 70)

        print("\nGenerated Code:\n")
        print(code)

        print("\nExecuting code...")

        result = execute_code(code)

        # Save attempt information
        log_attempt(
            attempt,
            code,
            result
        )

        # Show output
        if result["stdout"]:
            print("\nOutput:")
            print(result["stdout"])

        # Show error
        if result["stderr"]:
            print("\nError:")
            print(result["stderr"])

        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        if result["passed"]:

            print("\n" + "=" * 70)
            print("SUCCESS - CODE PASSED")
            print("=" * 70)

            return True

        # --------------------------------------------------
        # FAILURE
        # --------------------------------------------------

        print("\nFAILED")

        # If attempts are still available
        if attempt < MAX_ATTEMPTS:

            print("\nSending error back to the LLM...")
            print("The agent will try to fix the code.")

            error_message = result["stderr"]

            if result["stdout"]:
                error_message += (
                    "\n\nProgram output:\n"
                    + result["stdout"]
                )

            # Ask LLM to fix the failed code
            code = fix_code(
                task,
                code,
                error_message
            )

        else:

            print("\n" + "=" * 70)
            print("FAILED - MAXIMUM ATTEMPTS REACHED")
            print("=" * 70)

            return False


def main():

    print("\n" + "=" * 70)
    print("WEEK 2 - EXECUTE, OBSERVE, SELF-CORRECT")
    print("=" * 70)

    task = input(
        "\nEnter your programming task:\n> "
    )

    if not task.strip():

        print("\nTask cannot be empty.")
        return

    run_agent(task)


if __name__ == "__main__":
    main()