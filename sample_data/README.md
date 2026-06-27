# sample_data/

Place your chat history file here for memory import:

```
sample_data/
└── gpt_chat_history.txt   ← one message per line
```

Then call `POST /memory_reload` to import it into ChromaDB.

This directory is excluded from git (see `.gitignore`).
