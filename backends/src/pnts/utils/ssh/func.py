"""
module description:

ssh funcs
"""

from enum import Enum
import os
from pathlib import Path
from paramiko import (
    PKey,
    RSAKey,
    DSSKey,
    Ed25519Key,
    ECDSAKey,
)


def resolve_ssh_dir():
    # Determine the user's home directory based on the operating system
    if os.name == "posix":  # Unix-based systems (MacOS and Linux)
        home_dir = Path(os.path.expanduser("~"))
    elif os.name == "nt":  # Windows
        home_dir = Path(os.path.expandvars("%userprofile%"))
    else:
        # Handle other operating systems if needed
        raise OSError("Unsupported operating system")

    ssh_dir = home_dir / ".ssh"

    return ssh_dir


def resolve_key_path(key_path: str, proj_dir: str | None = None) -> Path:
    if proj_dir is None:
        proj_dir = Path(__file__).resolve().parent

    possible_paths = [
        Path(key_path),
        proj_dir / key_path,
        resolve_ssh_dir() / key_path,
    ]

    for path in possible_paths:
        if path.is_file():
            return path

    raise FileNotFoundError("The `ssh_key` file is not found.")


class SSHKeyType(Enum):
    RSA = RSAKey
    DSS = DSSKey
    Ed25519 = Ed25519Key
    ECDSA = ECDSAKey


def get_ssh_key(ssh_key: tuple[str, str]) -> PKey | None:
    try:
        key_filepath: Path | None = resolve_key_path(ssh_key[0]) if ssh_key[0] else None
    except (IOError, FileNotFoundError):
        return None

    if key_filepath:
        ssh_key = (
            SSHKeyType[ssh_key[1]].value.from_private_key_file(
                str(key_filepath)
            )
            if ssh_key[1]
            else None
        )
        return ssh_key

    return None
