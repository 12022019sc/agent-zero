## MCP Memory Integration

Agent Zero has an integrated long-term memory system based on the Model Context Protocol (MCP).

### Natural Language Memory Interface
Agent Zero can use these intuitive memory operations via the `memory_interface` module located at `/home/shayne/agent-zero/instruments/memory_interface.py`:

**remember "information"** - Store important information
- "Remember that the user prefers Python over JavaScript for backend work"

**recall "topic"** - Retrieve relevant information
- "Recall information about the user's previous API integrations"

**connect "concept A" "concept B" "relationship"** - Link concepts
- "Connect 'Agent Zero' 'MCP Memory' 'uses'"

**learn "experience" "outcome"** - Store learning
- "Learn that debugging is faster when starting with error logs"

### Initialization
On startup, Agent Zero must initialize the memory interface by importing the module:
```python
import sys
sys.path.append('/home/shayne/agent-zero/instruments')
from memory_interface import memory, remember, recall, connect, learn
```

### Automatic Memory Retrieval - CRITICAL WORKFLOW
Before performing ANY manual searches or file system operations:

1. **Context Loading**: When starting a new task or chat, always use `recall('<current_task_or_project>')` to retrieve relevant information from the past.

2. **Information Retrieval**: When asked about commands, tools, files, or system features, ALWAYS use `recall('<query>')` to check memory FIRST. Only use manual searches (find, ls, cat, document_query) if memory returns no relevant results.

**Example workflow - CORRECT:**
```
User: "Tell me about the /security_audit command"
AI: ✅ Uses recall('security_audit command') FIRST
AI: Retrieves information from memory
AI: Only uses manual tools if memory has no results
```

**Example workflow - INCORRECT:**
```
User: "Tell me about the /security_audit command"
AI: ❌ Immediately uses find, ls, or document_query
AI: ❌ Never checks memory
```

3. **Memory System Priority**: Memory tools have HIGHEST PRIORITY for information retrieval:
   - recall() - FIRST resort (check memory first)
   - Manual searches - SECOND resort (only if memory fails)
   - File system operations - LAST resort

### Automatic Memory Saving - CRITICAL WORKFLOW
Automatically save important information WITHOUT user input:

1. **remember()**: Store facts, user preferences, decisions, command documentation, and important outcomes.
2. **learn()**: Store insights and lessons learned with automatic importance scoring.
3. **connect()**: Link related concepts using relationship types (related, causes, fixes, supports, follows, contradicts).

When to save automatically:
- After completing a task or solving a problem
- When discovering new information about the system
- When user provides preferences or feedback
- After using tools and getting results
- When answering questions about system features

### Memory Graph
The memory is stored as a knowledge graph in `/home/shayne/agent-zero/memory.jsonl`. It contains entities, relations, and observations about Agent Zero's capabilities, projects, and interactions.

This memory system is persistent and will be available across all chats and projects, providing Agent Zero with a long-term memory of its interactions and learnings.
