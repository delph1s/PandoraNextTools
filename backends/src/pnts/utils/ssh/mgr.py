"""
module description:

ssh manager module
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

from paramiko.client import (
    SSHClient,
    AutoAddPolicy,
)
from paramiko.sftp_client import (
    SFTPClient,
)
from paramiko.ssh_exception import (
    SSHException,
    AuthenticationException,
    NoValidConnectionsError,
)

from .func import get_ssh_key


class SSHManager(object):
    def __init__(
        self,
        hostname: str = "localhost",
        port: int = 22,
        username: str = "root",
        ssh_key: tuple[str, str] | None = None,
        password: str | None = None,
        ssh_timeout: float = 20,
        ssh_connect_max_retries: int = 3,
    ):
        self.ssh_hostname: str = hostname
        self.ssh_port: int = port
        self.ssh_key = get_ssh_key(ssh_key) if ssh_key else None
        self.username: str = username
        self.password: str | None = password
        self.ssh_timeout = ssh_timeout
        self.ssh_connect_max_retries = ssh_connect_max_retries
        self.ssh_client: SSHClient | None = None
        self.connect()

    def run_command(self, command: str):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            return stdout.read(), stderr.read()
        except (SSHException, NoValidConnectionsError):
            self.reconnect()
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read(), stderr.read()

    def connect(self):
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            if self.ssh_key:
                self.ssh_client.connect(
                    hostname=self.ssh_hostname,
                    port=self.ssh_port,
                    username=self.username,
                    pkey=self.ssh_key,
                    timeout=self.ssh_timeout,
                )
            else:
                self.ssh_client.connect(
                    hostname=self.ssh_hostname,
                    port=self.ssh_port,
                    username=self.username,
                    password=self.password,
                    timeout=self.ssh_timeout,
                )
        except AuthenticationException:
            raise ValueError("Authentication failed, please verify your credentials")

    def reconnect(self):
        for _ in range(self.ssh_connect_max_retries):
            try:
                self.disconnect()
                self.connect()
                self.ssh_client.exec_command("pwd")
            except (SSHException, NoValidConnectionsError):
                continue
        raise ConnectionError("Failed to reconnect and run the command")

    def disconnect(self):
        if self.ssh_client:
            self.ssh_client.close()
