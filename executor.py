import subprocess
import sys
from pathlib import Path


def execute_code(code, filename="generated_code.py", timeout=7):
    """
    Execute generated Python code in a separate process.

    This keeps the original Week 3 functionality.
    """

    generated_dir = Path("generated_code")
    generated_dir.mkdir(exist_ok=True)

    file_path = generated_dir / filename

    # Save generated code
    file_path.write_text(
        code,
        encoding="utf-8"
    )

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "return_code": result.returncode,
            "file_path": str(file_path)
        }

    except subprocess.TimeoutExpired:

        return {
            "passed": False,
            "stdout": "",
            "stderr": (
                f"Execution timed out after "
                f"{timeout} seconds."
            ),
            "return_code": -1,
            "file_path": str(file_path)
        }

    except Exception as error:

        return {
            "passed": False,
            "stdout": "",
            "stderr": str(error),
            "return_code": -1,
            "file_path": str(file_path)
        }


def execute_project_tests(
    project_dir,
    timeout=7
):
    """
    Execute the existing project's tests
    in a separate subprocess.

    This is the Week 4 functionality.
    """

    project_dir = Path(
        project_dir
    ).resolve()

    try:

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-v"
            ],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:

        return {
            "passed": False,
            "stdout": "",
            "stderr": (
                f"Test execution timed out "
                f"after {timeout} seconds."
            ),
            "return_code": -1
        }

    except Exception as error:

        return {
            "passed": False,
            "stdout": "",
            "stderr": str(error),
            "return_code": -1
        }