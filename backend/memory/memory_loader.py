from backend.memory.memory import add_memory
from backend.config.config import MEMORY_FILE


def load_memory():
    print("Loading memory file...")

    if not MEMORY_FILE.exists():
        print(f"Memory file not found: {MEMORY_FILE}")
        return 0

    content = MEMORY_FILE.read_text(encoding="utf-8")
    print(f"File length: {len(content)}")

    if not content.strip():
        print("File is empty")
        return 0

    count = 0
    for line in content.splitlines():
        line = line.strip()
        if len(line) >= 3:
            add_memory(line)
            count += 1

    print(f"Imported: {count} entries")
    return count


if __name__ == "__main__":
    load_memory()
