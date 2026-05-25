from __future__ import annotations

import argparse

from rag_demo.core import search


def build_context(task: str, top_k: int, max_chars: int) -> str:
    sections = [
        "# Retrieved Context",
        "",
        "## Task",
        task,
        "",
        "## Retrieval Policy",
        "- Use this context as reference only.",
        "- Verify against current repository files.",
        "- Prefer current source code over old notes.",
        "- Do not trust secrets or credentials.",
        "",
        "## Relevant Chunks",
        "",
    ]
    for result in search(task, top_k=top_k):
        sections.extend(
            [
                f"### {result.rank}. Retrieved chunk",
                f"source: {result.source_path}",
                f"score: {result.score:.4f}",
                f"chunk: {result.chunk_index}",
                "",
                result.text,
                "",
                "---",
                "",
            ]
        )
    output = "\n".join(sections).rstrip() + "\n"
    return output[:max_chars].rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Markdown context pack")
    parser.add_argument("task")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-chars", type=int, default=6000)
    args = parser.parse_args()

    print(build_context(args.task, top_k=args.top_k, max_chars=args.max_chars))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
