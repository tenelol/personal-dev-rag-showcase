# Personal Developer Memory RAG

個人用Developer Memory RAGの設計を、公開できる形にsanitizeしたshowcase repositoryです。

実運用版はprivateです。このrepositoryには、実データ、個人メモ、NASパス、privateまたはroutableなIPアドレス、ユーザー名、APIキー、token、credential、private keyは含めていません。面接やポートフォリオで「どういう思想で、どう安全に、どう使えるように作ったか」を短時間で説明するための公開版です。

## 概要 / Overview

このprojectは、開発メモやREADMEをローカルでindexし、AI coding agentに渡しやすいcontext packを生成するRAG pipelineを示します。

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

この公開版では、依存なしで動く最小demoとして、deterministic hashing embedder と JSONL store を使っています。実運用では同じ境界を保ったまま、Qdrantなどのlocal vector databaseや、より強いembedding modelに差し替えられる構成です。

## 背景 / Motivation

AI coding agentに大量のメモを常時渡すと、古い情報や不要な情報が混ざりやすくなります。このRAGでは、必要な時だけ少量の出典付きcontextを取得することを重視しています。

- index対象はcuratedなMarkdown/textだけに限定する
- 検索結果には必ずsource pathを出す
- context packはtaskごとに小さく生成する
- privateな運用情報は公開repoに含めない
- RAGの出力は参考情報として扱い、現在のsource codeを優先する

## アーキテクチャ / Architecture

詳細は [docs/architecture.md](docs/architecture.md) を参照してください。

主要component:

- `loader`: Markdown/text/READMEを探索し、secretやbinaryを除外する
- `chunker`: documentを小さなchunkへ分割し、metadataを付ける
- `embedder`: textをvectorへ変換する
- `store`: vectorとmetadataを保存し、類似検索する
- `search`: rank、score、source path付きで検索結果を表示する
- `context`: 検索結果をCodexなどに渡しやすいMarkdownへ整形する

## 機能 / Features

- Markdown、text、READMEの再帰index
- `.env`、`.ssh`、`.git`、private key、credential、build output、cache、binary fileの明示除外
- dependency-freeなdemo CLI
- source path、score、chunk index付きの検索結果
- Markdown context pack生成
- Qdrantをlocalhost限定で起動するexample compose
- 公開版とprivate実運用版を分けるsecurity design
- 他の人がforkして自分用RAGへ流用できる構成

## 技術スタック / Tech Stack

- Python
- Qdrant想定のvector store design
- Docker Compose
- Markdown
- MCP-compatibleなtool設計

## セキュリティ設計 / Security Design

このrepositoryはsanitized showcaseです。以下は含めません。

- 実際のknowledge base本文
- 実NASパスやprivate infrastructure名
- privateまたはroutableなIPアドレス
- ユーザー名
- API key
- token
- credential
- private key
- `.env`

Qdrant exampleは `127.0.0.1` にbindし、public internetへ公開しない設計です。

詳細は [docs/security.md](docs/security.md) を参照してください。

## デモコマンド / Demo Commands

依存なしdemo:

```bash
python -m rag_demo.index --source data/sample_notes
python -m rag_demo.search "React form typing" --top-k 3
python -m rag_demo.context "Build a typed React form" --top-k 3
```

Makefileを使う場合:

```bash
make demo
```

Qdrant example:

```bash
cp .env.example .env
docker compose -f docker-compose.example.yml up -d
```

demo CLI自体はQdrantを必要としません。`docker-compose.example.yml` は、実運用でlocal vector databaseを使う場合の公開可能な設定例です。

## 自分用RAGとして流用する / Reuse As Your Own RAG

このrepositoryはforkして自分用RAGの土台として使えます。

1. Forkまたはcloneする
2. `data/sample_notes/` を自分のsyntheticまたは公開可能なメモに差し替える
3. private notesは別の非公開directoryで管理する
4. `.env.example` を参考に `.env` を作る
5. `python -m rag_demo.index --source <your-notes>` で試す
6. 必要になったらJSONL storeをQdrant-backed storeへ差し替える
7. AI coding agent連携が必要になったらMCP serverを追加する

詳しい流用手順は [docs/reuse-guide.md](docs/reuse-guide.md) を参照してください。

## 現在の状態 / Current Status

このrepositoryは公開showcaseです。

- Architectureとsecurity modelを文書化済み
- sample notesはsynthetic
- 最小demo実装あり
- Qdrant example設定あり
- 実運用データとprivate deployment詳細は意図的に除外

## 今後の予定 / Future Roadmap

- Qdrant-backed sample implementationを追加する
- MCP server exampleを追加する
- retrieval qualityのfixtureと評価を追加する
- CLI出力とcontext packのsanitized screenshotを追加する
- CIでdemo commandとsecret scanを実行する

詳細は [docs/roadmap.md](docs/roadmap.md) を参照してください。

## ライセンス / License

MIT License. See [LICENSE](LICENSE).
