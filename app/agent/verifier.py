from app.tools.tool_result import ToolResult


def verify_tool_result(
    tool_name: str,
    result: ToolResult,
) -> dict:

    if not result.success:

        return {
            "verified": False,
            "reason": (
                f"Tool '{tool_name}' failed."
            ),
            "evidence": result.error,
        }

    if result.data is None:

        return {
            "verified": False,
            "reason": (
                f"Tool '{tool_name}' returned "
                "no data."
            ),
            "evidence": None,
        }

    return {
        "verified": True,
        "reason": (
            f"Tool '{tool_name}' returned "
            "valid data."
        ),
        "evidence": result.data,
    }