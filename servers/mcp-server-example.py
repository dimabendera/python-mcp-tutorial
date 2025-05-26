"""
fastmcp run servers/mcp-server-example.py
"""

from fastmcp import FastMCP

mcp = FastMCP("Простий приклад 🚀")

@mcp.tool()
def return_pi() -> float:
    """Повертає число PI"""
    return 3.1415926


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


if __name__ == "__main__":
    mcp.run()
