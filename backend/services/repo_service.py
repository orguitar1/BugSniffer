import tempfile
import subprocess


def clone_repository(repository_url: str) -> str:
    temp_dir = tempfile.mkdtemp()

    subprocess.run(
        ["git", "clone", repository_url, temp_dir],
        check=True
    )

    return temp_dir