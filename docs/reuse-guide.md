# Reuse Guide

このrepositoryは、個人用Developer Memory RAGを作るための公開可能な土台として流用できます。

## 1. まずforkする

GitHubでforkするか、templateとしてcloneしてください。

```bash
git clone https://github.com/YOUR_NAME/personal-dev-rag-showcase.git
cd personal-dev-rag-showcase
```

## 2. sample notesを差し替える

公開repoに置いてよいsyntheticなメモだけを `data/sample_notes/` に置きます。

privateなメモはこのrepositoryに入れず、別のprivate directoryで管理してください。

安全な例:

- 公開してよい技術メモ
- demo用に作った架空の開発メモ
- READMEや設計メモのtemplate

避けるもの:

- private projectの本文
- 顧客情報
- private repository URL
- API key、token、password、credential
- 実NASパス、IPアドレス、ユーザー名

## 3. demoを動かす

```bash
python -m rag_demo.index --source data/sample_notes
python -m rag_demo.search "React form typing" --top-k 3
python -m rag_demo.context "Build a typed React form" --top-k 3
```

または:

```bash
make demo
```

## 4. 自分用のprivate knowledge rootを決める

本格運用では、公開repoとは別にprivateなknowledge rootを用意します。

例:

```text
knowledge/
├── notes/
├── dev-logs/
├── project-docs/
└── manuals/
```

重要なのは、home directory全体やNAS全体をindexしないことです。RAGに入れる文書はcuratedな領域に限定してください。

## 5. Qdrantへ差し替える

まずはexample composeを使ってlocal Qdrantを起動します。

```bash
cp .env.example .env
docker compose -f docker-compose.example.yml up -d
```

この公開版のdemoはJSONL storeですが、次の境界を維持するとQdrantへ移行しやすくなります。

- `embed(text) -> vector`
- `upsert(chunks)`
- `search(query_vector, top_k)`
- metadataに `source_path` と `chunk_index` を必ず保持する

## 6. AI coding agentと連携する

MCPを使う場合は、次のようなtoolから始めると十分です。

- `search_memory(query, top_k)`
- `get_context_for_task(task, top_k, max_chars)`

最初からWeb UI、自動同期、PDF取り込み、local LLMまで入れる必要はありません。まずはMarkdown/textを安全に検索できる状態を作るのが実用的です。

## 7. 公開前チェック

公開前に最低限確認してください。

```bash
find . \( -name .env -o -name __pycache__ -o -name .rag_demo \) -print
git status --short
```

private path、ユーザー名、IPアドレス、host名はprojectごとに形が違うため、追加で目視確認してください。必要ならsecret scannerも使ってください。
