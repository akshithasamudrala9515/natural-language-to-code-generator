from datetime import datetime
from pathlib import Path


def apply_file_changes(project_dir, changes):
    """
    Apply coordinated edits to project files.

    Each change must contain:
        path: Relative file path
        content: Complete replacement file content

    Original files are backed up before modification.
    """

    root = Path(project_dir).resolve()

    backup_root = root.parent / "backups" / (
        datetime.now().strftime("%Y%m%d_%H%M%S")
    )

    applied_files = []

    for change in changes:

        relative_path = Path(change["path"])

        if relative_path.is_absolute():
            raise ValueError(
                "Absolute paths are not allowed."
            )

        target = (root / relative_path).resolve()

        # Prevent writing outside the project directory.
        if not target.is_relative_to(root):
            raise ValueError(
                f"File path escapes project directory: "
                f"{relative_path}"
            )

        if target.suffix != ".py":
            raise ValueError(
                "Only Python files can be modified."
            )

        content = change["content"]

        if not isinstance(content, str):
            raise TypeError(
                "File content must be a string."
            )

        # Create a backup if the file already exists.
        if target.exists():

            backup_path = backup_root / relative_path
            backup_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            backup_path.write_bytes(target.read_bytes())

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.write_text(
            content,
            encoding="utf-8"
        )

        applied_files.append(str(relative_path))

    return {
        "applied_files": applied_files,
        "backup_directory": str(backup_root),
    }