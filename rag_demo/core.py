from __future__ import annotations

import hashlib
import json
import math
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


INDEX_PATH = Path(".rag_demo/index.jsonl")
SUPPORTED_SUFFIXES = {".md", ".txt"}
EXCLUDED_DIRS = {
    ".cache",
    ".git",
    ".ssh",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
    "venv",
}
EXCLUDED_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
EXCLUDED_NAMES = {"id_rsa", "id_ed25519", "credentials", "credentials.json"}


@dataclass(frozen=True)
class Chunk:
    source_path: str
    file_name: str
    file_type: str
    chunk_index: int
    content_hash: str
    updated_at: str
    text: str
    vector: list[float]


@dataclass(frozen=True)
class SearchResult:
    rank: int
    score: float
    source_path: str
    chunk_index: int
    text: str


def is_excluded_path(path: Path) -> bool:
    for part in path.parts:
        lowered = part.lower()
        if lowered in EXCLUDED_DIRS:
            return True
    name = path.name.lower()
    if name == ".ds_store" or name.startswith("._"):
        return True
    if name.startswith(".env"):
        return True
    if name in EXCLUDED_NAMES:
        return True
    if "token" in name or "secret" in name or "credential" in name:
        return True
    return path.suffix.lower() in EXCLUDED_SUFFIXES


def is_supported(path: Path) -> bool:
    return path.name == "README" or path.name.lower() == "readme.md" or path.suffix.lower() in SUPPORTED_SUFFIXES


def is_binary(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:4096]
    except OSError:
        return True
    if b"\x00" in sample:
        return True
    try:
        sample.decode("utf-8")
    except UnicodeDecodeError:
        return True
    return False


def discover_documents(source: Path) -> list[Path]:
    source = source.expanduser()
    if source.is_file():
        return [source] if not is_excluded_path(source) and is_supported(source) and not is_binary(source) else []

    found: list[Path] = []
    for root, dirnames, filenames in os.walk(source):
        root_path = Path(root)
        dirnames[:] = sorted(name for name in dirnames if not is_excluded_path(root_path / name))
        for filename in sorted(filenames):
            path = root_path / filename
            if is_excluded_path(path) or not is_supported(path) or is_binary(path):
                continue
            found.append(path)
    return found


def split_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    cleaned = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunks.append(cleaned[start:end].strip())
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
    return chunks


def embed(text: str, dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    tokens = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:4], "big") % dimensions
        vector[bucket] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def build_chunks(source: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in discover_documents(source):
        text = path.read_text(encoding="utf-8", errors="replace")
        updated_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat()
        try:
            source_path = str(path.resolve().relative_to(Path.cwd().resolve()))
        except ValueError:
            source_path = str(path)
        for index, chunk_text in enumerate(split_text(text)):
            content_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
            chunks.append(
                Chunk(
                    source_path=source_path,
                    file_name=path.name,
                    file_type="markdown" if path.suffix.lower() == ".md" or path.name == "README" else "text",
                    chunk_index=index,
                    content_hash=content_hash,
                    updated_at=updated_at,
                    text=chunk_text,
                    vector=embed(chunk_text),
                )
            )
    return chunks


def write_index(chunks: list[Chunk], index_path: Path = INDEX_PATH) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")


def read_index(index_path: Path = INDEX_PATH) -> list[Chunk]:
    if not index_path.is_file():
        raise FileNotFoundError("Index not found. Run: python -m rag_demo.index --source data/sample_notes")
    chunks: list[Chunk] = []
    with index_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            chunks.append(Chunk(**payload))
    return chunks


def search(query: str, top_k: int = 5) -> list[SearchResult]:
    query_vector = embed(query)
    scored = [
        (cosine(query_vector, chunk.vector), chunk)
        for chunk in read_index()
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        SearchResult(
            rank=rank,
            score=score,
            source_path=chunk.source_path,
            chunk_index=chunk.chunk_index,
            text=chunk.text,
        )
        for rank, (score, chunk) in enumerate(scored[:top_k], start=1)
    ]


def preview(text: str, max_chars: int = 240) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= max_chars else compact[: max_chars - 3] + "..."
