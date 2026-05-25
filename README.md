# Personal Developer Memory RAG

A sanitized showcase of a private developer-memory RAG system for local coding
workflows.

The production system is private and contains no data from this repository. This
showcase keeps the architecture, safety model, and developer experience visible
without publishing private notes, internal paths, private or routable IP
addresses, usernames, credentials, or operational secrets.

## Overview

This project demonstrates a local-first RAG pipeline for developer notes:

1. Read curated Markdown and text documents.
2. Exclude secrets, build output, binary files, and broad unreviewed folders.
3. Split documents into auditable chunks.
4. Embed chunks and store them in a vector database.
5. Search by task and generate a compact, source-backed context pack for an AI
   coding agent.

The sample implementation in this repository is intentionally minimal. It uses a
deterministic local hashing embedder and a JSON file store so the demo can run
without cloud credentials. The production implementation uses the same
boundaries with a local vector database and optional stronger embedding models.

## Motivation

AI coding tools work better when they can retrieve the right context at the right
time. Large, always-on prompts are hard to audit and often pollute the model
context. This system keeps memory explicit:

- Only curated files are indexed.
- Search results always include source paths.
- Context packs are small and task-specific.
- Private operational data stays out of the public showcase.

## Architecture

```text
curated notes
    |
    v
loader -> chunker -> embedder -> vector store
                                      |
                                      v
                         search CLI / context pack CLI
                                      |
                                      v
                              coding agent context
```

See [docs/architecture.md](docs/architecture.md) for the full design.

## Features

- Recursive indexing for Markdown, text, and README files.
- Explicit denylist for `.env`, `.ssh`, `.git`, private keys, credentials,
  build artifacts, caches, and binary files.
- Deterministic demo embeddings for offline reproducibility.
- Source-backed search results with score and chunk index.
- Markdown context pack generation for coding tasks.
- Local-only vector database configuration example.
- Security documentation for public/private separation.

## Tech Stack

- Python for CLI and RAG pipeline boundaries.
- Qdrant as the intended local vector database.
- Docker Compose for local service orchestration.
- Markdown for knowledge documents and generated context packs.
- MCP-compatible architecture for AI coding agent integration.

## Security Design

This repository is a sanitized showcase. It intentionally excludes:

- real knowledge base content
- private infrastructure names
- private NAS paths
- usernames
- private or routable IP addresses
- API keys
- credentials
- tokens
- private keys

The indexing policy is deny-by-default for sensitive paths and binary files.
Services are designed to bind to localhost unless explicitly changed.

See [docs/security.md](docs/security.md) for details.

## Demo Commands

Run the dependency-free demo:

```bash
python -m rag_demo.index --source data/sample_notes
python -m rag_demo.search "React form typing" --top-k 3
python -m rag_demo.context "Build a typed React form" --top-k 3
```

Optional Qdrant example:

```bash
cp .env.example .env
docker compose -f docker-compose.example.yml up -d
```

The demo CLI does not require Qdrant. The compose file shows how the production
shape binds Qdrant to localhost only.

## Current Status

This public repository is a showcase artifact:

- Architecture and security model are documented.
- Sample notes are synthetic and safe.
- Minimal local demo is included.
- Production data, production configuration, and private deployment details are
  intentionally omitted.

## Future Roadmap

- Add a full Qdrant-backed sample implementation.
- Add MCP server example tools for `search_memory` and `get_context_for_task`.
- Add evaluation fixtures for retrieval quality.
- Add screenshots of CLI output and context pack workflow.
- Add CI checks for secret scanning and sample demo commands.

See [docs/roadmap.md](docs/roadmap.md).
