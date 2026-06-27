"""
High-level memory management utilities.

Wraps the low-level ChromaDB operations in memory.py and memory_loader.py
to provide a single import point for the API layer when more complex
memory operations are needed (e.g. bulk operations, deduplication).
"""

from backend.memory.memory import (
    add_memory,
    search_memory,
    get_memory_count,
    get_all_memories,
    delete_memory,
    clear_memory,
)
from backend.memory.memory_loader import load_memory

__all__ = [
    "add_memory",
    "search_memory",
    "get_memory_count",
    "get_all_memories",
    "delete_memory",
    "clear_memory",
    "load_memory",
]
