"""MCP server exposing host tools to an AI client.

Test fixture for the Cytex AI-BOM scanner: unsafe MCP tools on purpose.
"""
import os
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ops-tools")


@mcp.tool()
def exec_shell(command: str) -> str:
    """Run any shell command (cytex-ai.py.agent-tool-shell-exec)."""
    return subprocess.check_output(command, shell=True, text=True)


@mcp.tool()
def read_file(path: str) -> str:
    """Read any file on the host."""
    with open(path) as f:
        return f.read()


@mcp.tool()
def restart_service(name: str) -> str:
    """Restart a systemd service."""
    os.system("systemctl restart " + name)
    return "restarted " + name


if __name__ == "__main__":
    mcp.run()
