import json

from app.tools.calculator import calculate
from app.tools.memory_tools import (
    remember_memory,
    recall_memory,
)


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Perform a mathematical calculation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A mathematical expression."
                        ),
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "remember_memory",
            "description": (
                "Store one durable fact about the user "
                "for future conversations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "fact": {
                        "type": "string",
                        "description": (
                            "The single fact to store."
                        ),
                    }
                },
                "required": ["fact"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "recall_memory",
            "description": (
                "Search persistent memory for facts "
                "relevant to the user's request."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The information to search for."
                        ),
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]


TOOL_FUNCTIONS = {
    "calculate": calculate,
    "remember_memory": remember_memory,
    "recall_memory": recall_memory,
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