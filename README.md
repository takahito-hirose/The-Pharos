# 🗼 The Pharos (ARK Quality Audit System)

The Pharos（ファロス）は、自律型AIエージェントシステム「ARK」のために建造された、独立した**マルチファイル対応のコード品質監査システム**です。
ローカルのAPIサーバーとして稼働するだけでなく、**カスタム GitHub Action** としても機能し、あらゆるリポジトリのPRに対して自動でAIレビューを実行します。

## 👁️ Philosophy (思想)
**"AI must be audited by AI."**
人間が介在しない自律開発（Phase 17：夜間航行）において、生成されたコードの品質を担保するのは、人間ではなく「独立した公正なAIの目」であるべきだという信念のもとに設計されました。

## 📊 Quality Pentagram (5軸評価)
The Pharosは、単なる文法チェックを超え、ファイル間の文脈やアーキテクチャの整合性を含めた以下の5つの次元でコードを多角的に採点します。

1. **Security:** 脆弱性やシークレットの混入、パス・トラバーサル等のリスク検知。
2. **Performance:** アルゴリズムの効率性やリソース消費の最適化。
3. **Maintainability:** 命名規則、SOLID原則、技術的負債の有無。
4. **Resilience:** 例外処理、リトライロジック、エラー回復力の評価。
5. **Testability:** モックのしやすさ、密結合の回避、テストコードの書きやすさ。

---

## 🐙 Usage as GitHub Action (推奨)

The Pharos は、あなたのプロジェクトのCI/CDパイプラインに簡単に組み込むことができます。
PRが作成・更新された際、変更されたPythonファイルを自動で検知し、一括でコンテキスト監査を行い、PRのコメントに5軸のレーダーチャート（スコア）と指摘事項を投稿します。

### 導入手順
対象プロジェクトの `.github/workflows/pharos-audit.yml` に以下の設定を追加するだけです。

```yaml
name: 🗼 The Pharos Code Audit

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: 🚢 Checkout Repository
        uses: actions/checkout@v4
        
      - name: 🗼 Run The Pharos Audit
        uses: takahito-hirose/The-Pharos@main
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

**※注意:** 導入先のリポジトリの GitHub Secrets に `GEMINI_API_KEY` を登録してください。

---

## 💻 Local Development (ローカルAPIとしての起動)

The Pharos の挙動をテストしたり、ローカルエージェント（ARK等）の門番として使用する場合は、以下の手順でスタンドアロンのAPIサーバーとして起動できます。

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) (For Local LLM use) or Gemini API Key

### 2. Setup
```bash
git clone [https://github.com/takahito-hirose/The-Pharos.git](https://github.com/takahito-hirose/The-Pharos.git)
cd The-Pharos
python -m venv .venv
source .venv/bin/activate  # Mac/Linux (Windows: .\.venv\Scripts\activate)
pip install -r requirements.txt
```

### 3. Configuration
`.env` ファイルを作成し、使用するモデルを指定してください。
```env
GEMINI_API_KEY=your_api_key_here
REVIEW_MODEL=gemini/gemini-2.5-flash  # または ollama/gemma など
```

### 4. Customizing the Brain (プロンプトの調整)
LLMの評価基準やペルソナは、ソースコードではなく `prompts/reviewer_skills.md` に外出しされています。このMarkdownファイルを編集することで、監査の厳しさや着眼点を自由にチューニングできます。

### 5. Running the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## 🔌 API Endpoints (Local Mode)
- `POST /api/v1/audit/static`: Flake8による高速な静的解析 (`target_path` 指定).
- `POST /api/v1/audit/ai`: LLMを用いた5軸のディープ・レビュー。**複数のファイルパス** (`target_paths` リスト) を受け取り、相関関係を含めた一括監査を行います。

---
Produced by **ARK Autonomous Development Loop**.