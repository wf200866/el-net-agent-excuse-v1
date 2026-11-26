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


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(dir=OUTPUT_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(EXCUSE)
        # chmod the file we created, never the /output directory itself.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, OUTPUT_FILE)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
