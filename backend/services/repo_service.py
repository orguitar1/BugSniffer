import tempfile
import subprocess
import shutil
import logging

logger = logging.getLogger(__name__)


class RepoCloneError(Exception):
    pass


def clone_repository(repository_url: str) -> str:
    temp_dir = tempfile.mkdtemp()

    try:
        logger.info(f"Cloning repository: {repository_url}")

        subprocess.run(
            ["git", "clone", repository_url, temp_dir],
            check=True,
            capture_output=True,
            text=True
        )

        logger.info(f"Successfully cloned {repository_url} to {temp_dir}")
        return temp_dir

    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir, ignore_errors=True)

        error_msg = e.stderr.strip() or "Unknown git error"

        logger.error(f"Failed to clone {repository_url}: {error_msg}")
        raise RepoCloneError(
            f"Git clone failed for {repository_url}: {error_msg}"
        )