import json
from datetime import datetime, timezone
from pathlib import Path


MEMORY_FILE = Path("data/memory.json")


class MemoryStore:

    def __init__(self):
        MEMORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not MEMORY_FILE.exists():
            self._save({
                "memories": []
            })

    def _load(self) -> dict:
        with MEMORY_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _save(self, data: dict) -> None:
        temp_file = MEMORY_FILE.with_suffix(".tmp")

        with temp_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )

        temp_file.replace(MEMORY_FILE)

    def add(self, content: str) -> dict:
        content = content.strip()

        if not content:
            raise ValueError(
                "Memory cannot be empty."
            )

        data = self._load()

        memory = {
            "id": len(data["memories"]) + 1,
            "content": content,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        data["memories"].append(memory)

        self._save(data)

        return memory

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        data = self._load()

        query_words = {
            word.lower()
            for word in query.split()
            if len(word) >= 3
        }

        scored = []

        for memory in data["memories"]:

            content = memory["content"].lower()

            score = sum(
                word in content
                for word in query_words
            )

            if score > 0:
                scored.append(
                    (score, memory)
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory
            for _, memory in scored[:limit]
        ]