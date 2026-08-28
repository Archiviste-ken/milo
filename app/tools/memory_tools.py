from app.memory.store import MemoryStore


memory_store = MemoryStore()


def remember_memory(fact: str) -> dict:
    """
    Save an important fact to persistent memory.
    """

    fact = fact.strip()

    if not fact:
        return {
            "success": False,
            "error": "Memory cannot be empty.",
        }

    try:
        memory = memory_store.add(fact)

        return {
            "success": True,
            "memory": memory,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }


def recall_memory(query: str) -> dict:
    """
    Search persistent memory for relevant information.
    """

    query = query.strip()

    if not query:
        return {
            "success": False,
            "error": "Query cannot be empty.",
        }

    try:
        results = memory_store.search(query)

        return {
            "success": True,
            "results": results,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
        }