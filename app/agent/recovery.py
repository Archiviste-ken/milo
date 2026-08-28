def should_retry(
    tool_name: str,
    result: dict,
) -> bool:

    if result.get("success"):
        return False

    error = (
        result.get("error") or ""
    ).lower()

    if "unknown tool" in error:
        return False

    if "permission" in error:
        return False

    if "division by zero" in error:
        return False

    return True