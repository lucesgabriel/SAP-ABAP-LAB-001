#!/usr/bin/env python
"""Smoke-test the exact secret-free Claude Desktop ARC-1 launcher."""
from __future__ import annotations

import asyncio
from pathlib import Path
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

NODE = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "node" / "node.exe"
LAUNCHER = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "integrations" / "claude" / "launch_arc1.mjs"


async def main() -> int:
    if not NODE.is_file() or not LAUNCHER.is_file():
        print("FAIL: launcher prerequisites missing")
        return 1
    params = StdioServerParameters(command=str(NODE), args=[str(LAUNCHER)])
    async with stdio_client(params) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            listed = await session.list_tools()
            names = sorted(tool.name for tool in listed.tools)
            expected = {"SAPRead", "SAPSearch", "SAPWrite", "SAPActivate", "SAPNavigate", "SAPLint", "SAPDiagnose", "SAPContext", "SAPManage", "SAPTransport", "SAPGit", "SAPQuery"}
            print(f"tools={len(names)}")
            print("tool_names=" + ",".join(names))
            missing = sorted(expected.difference(names))
            if missing:
                print("FAIL: missing tools=" + ",".join(missing))
                return 1
            result = await session.call_tool("SAPRead", {"type": "SYSTEM"})
            if result.is_error:
                print("FAIL: SAPRead SYSTEM returned an error")
                return 1
            print("sap_auth_read=PASS")
            return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
