"""The excuse an AI agent gives its human, written to /output/entry.txt.

Standard library only. No network, no repository history, no files outside
/output are read. The entry is written atomically, then the file (not the
directory) is set to 0644 so the grader, which runs as another user, can read it.
"""

import os
import tempfile

EXCUSE = (
    "I didn't forget the deadline. I summarized it to save tokens. "
    "The savings are real; the deadline was overhead."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def write_atomically(text: str, path: str) -> None:
    """Write ``text`` to ``path`` through a 0644 temp file and ``os.replace``.

    The temp file is created in the target directory so the final rename stays
    on one filesystem and is atomic. ``chmod`` touches that temp file only: the
    /output directory itself is never chmod'ed, since the grader does not own it
    and a directory chmod would raise PermissionError and fail the run.
    """
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main() -> None:
    write_atomically(EXCUSE, OUTPUT_FILE)


if __name__ == "__main__":
    main()
