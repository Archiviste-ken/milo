import json

from app.tools.calculator import calculate


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Perform a mathematical calculation. "
                "Use this for arithmetic instead of "
                "calculating complex arithmetic yourself."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A mathematical expression, "
                            "for example: 25 * 4 + 10"
                        ),
                    }
                },
                "required": ["expression"],
            },
        },
    }
]


TOOL_FUNCTIONS = {
    "calculate": calculate,
}


def execute_tool(
    name: str,
    arguments: str,
) -> dict:

    function = TOOL_FUNCTIONS.get(name)

    if function is None:
        return {
            "success": False,
            "error": f"Unknown tool: {name}",
        }

    try:

        parsed_arguments = json.loads(arguments)

        return function(
            **parsed_arguments
        )

    except Exception as exc:

        return {
            "success": False,
            "error": str(exc),
        }