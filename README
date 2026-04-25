# 🗼 The Pharos (ARK Quality Audit System)

The Pharos（ファロス）は、自律型AIエージェントシステム「ARK」のために建造された、独立した**コード品質監査API**です。

## 👁️ Philosophy (思想)
**"AI must be audited by AI."**
人間が介在しない自律開発（Phase 17：夜間航行）において、生成されたコードの品質を担保するのは、人間ではなく「独立した公正なAIの目」であるべきだという信念のもとに設計されました。

## 📊 Quality Pentagram (5軸評価)
The Pharosは、単なる文法チェックを超え、以下の5つの次元でコードを多角的に採点します。

1. **Security:** 脆弱性やシークレットの混入、パス・トラバーサル等のリスク検知。
2. **Performance:** アルゴリズムの効率性やリソース消費の最適化。
3. **Maintainability:** 命名規則、SOLID原則、技術的負債の有無。
4. **Resilience:** 例外処理、リトライロジック、エラー回復力の評価。
5. **Testability:** モックのしやすさ、密結合の回避、テストコードの書きやすさ。



## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) (For Local LLM use) or Gemini API Key

### 2. Setup
```bash
git clone [https://github.com/takahito-hirose/The-Pharos.git](https://github.com/takahito-hirose/The-Pharos.git)
cd The-Pharos
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configuration
`.env` ファイルを作成し、使用するモデルを指定してください。
```env
GEMINI_API_KEY=your_api_key_here
REVIEW_MODEL=gemini/gemini-2.5-flash  # または ollama/gemma など
```

### 4. Running the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔌 API Endpoints
- `POST /api/v1/audit/static`: Flake8による高速な静的解析。
- `POST /api/v1/audit/ai`: LLMを用いた5軸のディープ・レビュー。

---
Produced by **ARK Autonomous Development Loop**.