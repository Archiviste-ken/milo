from app.tools.tool_result import ToolResult


def decide_recovery(
    tool_name: str,
    result: ToolResult,
) -> dict:

    # ✅ Tool succeeded → nothing to recover.
    if result.success:
        return {
            "should_retry": False,
            "reason": "Tool succeeded.",
        }

    error = (
        result.error or ""
    ).lower()

    # ❌ These failures should NOT be automatically retried.
    unsafe_errors = {
        "division by zero",
        "permission denied",
        "unknown tool",
    }

    if any(
        unsafe_error in error
        for unsafe_error in unsafe_errors
    ):
        return {
            "should_retry": False,
            "reason": (
                "Automatic retry is not safe "
                "for this error."
            ),
        }

    # ✅ Other failures are potentially recoverable.
    return {
        "should_retry": True,
        "reason": (
            "The failure may be recoverable."
        ),
    }