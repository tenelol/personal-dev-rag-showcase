from __future__ import annotations

import argparse
from pathlib import Path

from rag_demo.core import build_chunks, write_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Index sanitized sample notes")
    parser.add_argument("--source", required=True, help="Directory or file to index")
    args = parser.parse_args()

    chunks = build_chunks(Path(args.source))
    write_index(chunks)
    print(f"indexed_chunks: {len(chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
