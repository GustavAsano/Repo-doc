from pathlib import Path
import zipfile
import tempfile
import re
import subprocess
import shutil
import tempfile
import requests
from io import BytesIO

import os
IN_DIR = Path(os.getenv("APP_DATA_DIR", "/app/data")) / "in"
IN_DIR.mkdir(parents=True, exist_ok=True)

def detect_source_type(source: str) -> str:
    source_path = Path(source)
    if re.match(r"https?://", source):
        return "git"
    if source.lower().endswith(".zip"):
        return "zip"
    if source_path.is_dir():
        return "folder"
    if source_path.is_file():
        return "file"
    raise ValueError("Unsupported source type")



def load_from_zip(zip_path: str) -> str:
    zip_path = Path(zip_path).resolve()
    repo_name = zip_path.stem
    target_dir = IN_DIR / repo_name
    owner = None

    # Remove existing copy
    if target_dir.exists():
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)

    return str(target_dir), repo_name, owner

def load_from_folder(folder_path: str) -> str:
    source = Path(folder_path).resolve()
    repo_name = source.name
    target_dir = IN_DIR / repo_name
    owner = None

    if target_dir.exists() and source == target_dir:
        return str(target_dir), repo_name, owner

    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(source, target_dir)

    return str(target_dir), repo_name, owner


def load_from_file(file_path: str) -> str:
    source = Path(file_path).resolve()
    if not source.is_file():
        raise ValueError("Invalid file path.")

    repo_name = source.stem
    target_dir = IN_DIR / repo_name
    owner = None

    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / source.name
    shutil.copy2(source, target_file)

    return str(target_dir), repo_name, owner


def load_from_git(git_url: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="repo_")
    subprocess.run(
        ["git", "clone", "--depth", "1", git_url, temp_dir],
        check=True
    )
    return temp_dir

def load_from_git(git_url: str) -> tuple[str, str, str]:
    """
    Download a public GitHub repository as a ZIP and extract it into in/<repo_name>
    """
    parts = git_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1].replace(".git", "")

    repo_name = repo
    target_dir = IN_DIR / repo_name

    if target_dir.exists():
        shutil.rmtree(target_dir)

    # Try main, master, then dev
    branches = ["main", "master", "dev", "develop"]
    response = None
    used_branch = None

    for branch in branches:
        url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                response = r
                used_branch = branch
                break
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"Cannot reach github.com — check that the backend container has outbound internet access."
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Request to GitHub timed out.")

    if response is None:
        raise RuntimeError(
            f"Could not find repository '{owner}/{repo}' on GitHub. "
            f"Tried branches: {', '.join(branches)}. "
            f"Make sure the URL is correct and the repo is public."
        )

    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(IN_DIR)

    extracted_dir = next(IN_DIR.glob(f"{repo}-*"), None)
    if extracted_dir is None:
        raise RuntimeError(f"Failed to extract repository ZIP for '{repo}'.")

    extracted_dir.rename(target_dir)

    return str(target_dir), repo, owner

def load_repository(source: str) -> str:
    source_type = detect_source_type(source)

    if source_type == "zip":
        return load_from_zip(source)
    elif source_type == "folder":
        return load_from_folder(source)
    elif source_type == "file":
        return load_from_file(source)
    elif source_type == "git":
        return load_from_git(source)
    else:
        raise ValueError("Unsupported source type")
