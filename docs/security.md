# Security

## Public Showcase Boundary

This repository is not the private production knowledge base. It contains only
synthetic examples, architecture notes, and a minimal demo implementation.

Do not commit:

- `.env`
- `.ssh`
- private keys
- API keys
- access tokens
- credentials
- private notes
- real infrastructure paths
- private or routable IP addresses
- usernames
- private repository URLs

## Indexing Policy

The indexer must never treat a broad directory as trusted input. Only curated
knowledge folders should be indexed.

The demo and production design exclude:

- `.env`, `.env.*`
- `.ssh`
- `.git`
- `node_modules`
- `dist`, `build`, `target`
- caches
- private key extensions such as `.pem` and `.key`
- known key names such as `id_rsa` and `id_ed25519`
- files with names containing `token`, `secret`, or `credential`
- binary files

## Service Exposure

Vector databases and local APIs should bind to localhost by default:

```yaml
ports:
  - "127.0.0.1:6333:6333"
```

Do not expose a personal-memory vector store to the public internet.

## Context Safety

Retrieved notes are advisory. An AI coding agent should:

- prefer current repository files over old notes
- show source paths
- keep context packs small
- avoid blindly trusting stale documents
- avoid storing generated context unless explicitly requested

## Sanitization Checklist

Before publishing:

- Search for private paths, usernames, private or routable IP addresses, and
  hostnames.
- Confirm there is no `.env` file.
- Confirm sample notes are synthetic.
- Confirm no real screenshots reveal private data.
- Run a secret scanner if available.
- Keep only `.env.example` with placeholder values.
