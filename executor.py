import subprocess
import sys
from pathlib import Path


def execute_code(code, filename="generated_code.py", timeout=7):
    """
    Safely execute generated Python code in a separate process.

    Returns:
        dict containing:
        - passed
        - stdout
        - stderr
        - return_code
    """

    generated_dir = Path("generated_code")
    generated_dir.mkdir(exist_ok=True)

    file_path = generated_dir / filename

    # Save generated code to a Python file
    file_path.write_text(code, encoding="utf-8")

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        passed = result.returncode == 0

        return {
            "passed": passed,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "return_code": result.returncode,
            "file_path": str(file_path)
        }

    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
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