from app.memory.store import MemoryStore
from app.tools.tool_result import ToolResult


memory_store = MemoryStore()


def remember_memory(fact: str) -> ToolResult:

    fact = fact.strip()

    if not fact:
        return ToolResult(
            success=False,
            error="Memory cannot be empty.",
        )

    try:
        memory = memory_store.add(fact)

        return ToolResult(
            success=True,
            data={
                "memory": memory,
            },
        )

    except Exception as exc:

        return ToolResult(
            success=False,
            error=str(exc),
        )


def recall_memory(query: str) -> ToolResult:

    query = query.strip()

    if not query:
        return ToolResult(
            success=False,
            error="Query cannot be empty.",
        )

    try:
        results = memory_store.search(query)

        return ToolResult(
            success=True,
            data={
                "results": results,
            },
        )

    except Exception as exc:

        return ToolResult(
            success=False,
            error=str(exc),
        )