from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from rag_demo.core import preview, search


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the demo RAG index")
    parser.add_argument("query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = search(args.query, top_k=args.top_k)
    if args.json:
        print(json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("No results.")
        return 0

    for result in results:
        print(f"{result.rank}. score={result.score:.4f}")
        print(f"source_path: {result.source_path}")
        print(f"chunk_index: {result.chunk_index}")
        print(f"preview: {preview(result.text)}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
