import tempfile
import subprocess
import shutil


class RepoCloneError(Exception):
    pass


def clone_repository(repository_url: str) -> str:
    temp_dir = tempfile.mkdtemp()

    try:
        subprocess.run(
            ["git", "clone", repository_url, temp_dir],
            check=True,
            capture_output=True,
            text=True
        )

        return temp_dir

    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir, ignore_errors=True)

        error_msg = e.stderr.strip() or "Unknown git error"

        raise RepoCloneError(
            f"Git clone failed for {repository_url}: {error_msg}"
        )