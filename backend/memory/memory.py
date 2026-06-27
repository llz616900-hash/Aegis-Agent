import chromadb
from backend.config.config import CHROMA_PATH

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="aegis_memory")


def add_memory(text):
    uid = str(abs(hash(text)))
    try:
        collection.add(ids=[uid], documents=[text])
    except Exception as e:
        print("add_memory:", e)


def search_memory(query, n=5):
    try:
        result = collection.query(query_texts=[query], n_results=n)
        return "\n".join(result["documents"][0])
    except Exception as e:
        print("search_memory:", e)
        return ""


def get_memory_count():
    try:
        return len(collection.get()["ids"])
    except Exception as e:
        print("get_memory_count:", e)
        return 0


def clear_memory():
    global collection
    try:
        client.delete_collection("aegis_memory")
    except Exception:
        pass
    collection = client.get_or_create_collection("aegis_memory")


def get_all_memories():
    try:
        data = collection.get()
        return {"ids": data["ids"], "documents": data["documents"]}
    except Exception as e:
        print(e)
        return {"ids": [], "documents": []}


def delete_memory(memory_id):
    try:
        collection.delete(ids=[memory_id])
        return True
    except Exception as e:
        print(e)
        return False
