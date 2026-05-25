# Architecture

## Goal

Build a local-first developer-memory RAG system that retrieves small,
source-backed context for coding tasks without exposing private notes or
infrastructure details.

## Non-Goals

- Indexing an entire home directory, drive, or NAS share.
- Publishing production notes or operational paths.
- Replacing repository source code as the source of truth.
- Injecting all memory into every AI prompt.

## Data Flow

```text
curated Markdown/text files
    |
    v
document discovery
    |
    v
secret and binary exclusion
    |
    v
chunking with metadata
    |
    v
embedding
    |
    v
local vector store
    |
    v
search results with source paths
    |
    v
Markdown context pack for a coding task
```

## Components

### Loader

Discovers supported documents and refuses sensitive or unsupported files.

Supported examples:

- `.md`
- `.txt`
- `README`
- `README.md`

Excluded examples:

- `.env`, `.env.*`
- `.ssh`
- `.git`
- private key files
- credentials files
- `node_modules`
- `dist`, `build`, `target`
- caches
- binary files

### Chunker

Splits documents into stable chunks and attaches metadata:

- `source_path`
- `file_name`
- `file_type`
- `chunk_index`
- `content_hash`
- `updated_at`

### Embedder

The showcase demo uses deterministic local hashing. A production deployment can
swap this for a stronger embedding provider while preserving the same interface.

### Store

The intended production store is Qdrant running locally. The showcase demo uses a
JSON file so it can run anywhere without secrets or infrastructure.

### Search

Search returns ranked chunks with score and source path. Results are not treated
as authority; the user or agent should verify them against current repository
files.

### Context Pack

The context pack command converts search results into compact Markdown:

```md
# Retrieved Context

## Task
Build a typed React form

## Retrieval Policy
- Use this context as reference only.
- Verify against current repository files.
- Prefer current source code over old notes.

## Relevant Chunks
...
```

## MCP Shape

The production design can be exposed as MCP tools:

- `search_memory(query, top_k)`
- `get_context_for_task(task, top_k, max_chars)`
- `remember_note(title, body, tags)`

For a public showcase, only the interface and sanitized behavior are shown.
