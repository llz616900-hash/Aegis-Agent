from fastapi import APIRouter

from backend.core.models import DeleteMemoryRequest
from backend.memory.memory import (
    get_all_memories,
    delete_memory,
    clear_memory,
    get_memory_count,
)
from backend.memory.memory_loader import load_memory

router = APIRouter(tags=["memory"])


@router.get("/memories")
def list_memories():
    """Return all stored memory entries (id + document text)."""
    return get_all_memories()


@router.get("/memory_count")
def memory_count():
    """Return the total number of memory entries."""
    return {"count": get_memory_count()}


@router.post("/memory_reload")
def memory_reload():
    """Re-import memory from sample_data/gpt_chat_history.txt into ChromaDB."""
    count = load_memory()
    return {"success": True, "imported": count}


@router.post("/delete_memory")
def delete_memory_endpoint(req: DeleteMemoryRequest):
    """Delete a single memory entry by its ID."""
    ok = delete_memory(req.memory_id)
    return {"success": ok}


@router.post("/memory_clear")
def memory_clear():
    """Wipe all memory entries from ChromaDB."""
    clear_memory()
    return {"success": True}
