from app.memory.store import MemoryStore


memory = MemoryStore()

saved = memory.add(
    "I am learning agentic engineering."
)

print("Saved:")
print(saved)

print("\nSearch result:")

results = memory.search(
    "agentic engineering"
)

for result in results:
    print(result)