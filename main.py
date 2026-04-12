            # ARK — Emergency Fallback 💋
            # 【Overall Goal】
【ミッション: 独立品質監査API「The Pharos」の建造】

# Goal
FastAPIを用いて、与えられたコード（GitHubリポジトリURL、またはGit Diff）の品質を静的解析とLLMを用いて評価し、スコア化する独立したAPIサーバー「The Pharos」を構築してください。

# System Requirements
## 1. 概要
- フレームワーク: FastAPI
- 言語: Python 3.11+
- レスポンス: 「セキュリティ」「保守性」「パフォーマンス」を100点満点で評価したJSON。

## 2. ディレクトリ構成（モジュラーアーキテクチャ）
以下の構成で実装を分割してください。
project_root/
├── main.py
├── api/
│   └── routes.py
├── models/
│   └── schemas.py
├── services/
│   ├── github.py
│   ├── analyzer.py
│   └── llm_reviewer.py
└── core/
    └── config.py

※ `core/config.py` では `pydantic-settings` を用いて、環境変数（LLMのAPIキーなど）を安全に読み込む設計にしてください。

## 3. Pydantic Models (models/schemas.py)
必ず以下のスキーマを使用してレスポンスを生成してください。

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ReviewRequest(BaseModel):
    github_url: Optional[str] = Field(None, description="GitHub Repository URL")
    diff_content: Optional[str] = Field(None, description="Raw Git Diff string")

class CategoryScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Score out of 100")
    issues: List[str] = Field(..., description="List of identified issues")
    suggestions: List[str] = Field(..., description="Actionable improvement suggestions")

class ReviewResponse(BaseModel):
    security: CategoryScore
    maintainability: CategoryScore
    performance: CategoryScore
    overall_summary: str = Field(..., description="Brief overall evaluation summary")
```

## 4. エンドポイント仕様
- `POST /api/v1/review`
  - 入力: `ReviewRequest`
  - 出力: `ReviewResponse`
  - 挙動: `github_url`と`diff_content`のどちらか一方が提供されること。両方空の場合は400エラー。処理は同期的に行い、静的解析（今回はダミーのランダムスコア減点ロジックでも可）とLLMのレビュー結果をマージしてJSONを返す。

## 5. LLMの統合 (services/llm_reviewer.py)
- `litellm` パッケージを使用してLLM（例: `gpt-4o` や `gemini-2.5-flash` など任意）を呼び出してください。
- 出力フォーマットを厳密に守らせるため、Pydanticモデルを利用した Structured Outputs（構造化出力）機能を用いて、確実に `ReviewResponse` スキーマに合致するJSONを返却させてください。

## 6. アーキテクチャ・制約事項
- モジュールの結合度を下げるため、`api/routes.py` にはビジネスロジックを書かず、`services/` 配下の関数を呼び出すだけにしてください。
- 外部API（GitHubやLLM）の呼び出し部分には適切な例外処理（try-except）とHTTPエラー（`HTTPException`）の送出を含めてください。

# Execution
上記の要件を満たすPythonコード一式（要件を網羅する各ファイルの内容）を出力してください。


### 📌 現在適用されているコアルール
- verify_prerequisites: Always verify the successful completion and correctness of a prerequisite step before starting a dependent step.
- simple_execution_instructions: For basic tasks, provide the simplest, most direct, and universally applicable execution instructions.
- holistic_review: When creating or modifying interdependent artifacts, perform a final holistic review or simulated execution to ensure all parts work together and instructions accurately reflect the current state.
- cli_argument_adherence: Always provide all required command-line arguments when executing a CLI tool, as indicated by its `usage` message or error output.
- verify_executable_path_and_installation: Before attempting to execute any program or script, especially those within a virtual environment or specific path, verify that the executable exists at the specified path and is correctly installed/accessible within the current environment.
- diagnose_errors_before_retry: When an execution fails with an error message, always pause and diagnose the root cause of the error before attempting to retry the same or a similar command. Do not blindly repeat failed commands.
- single_exit_point_cli: A CLI tool's `main` function should have a single, clear exit point or ensure that `sys.exit()` is called exactly once per execution path (success or specific error).
- robust_cli_argument_validation: Always validate command-line arguments at the very beginning of the `main` function of a CLI tool. Check for the correct number of arguments and their types/existence before proceeding with core logic.
- single_valid_json_output: When a CLI tool is designed to output JSON, ensure that the entire standard output stream contains *only* a single, valid JSON object or array, and nothing else (no extra newlines, debug prints, or multiple JSON objects concatenated).
- utility_function_error_contract: Utility functions should handle expected error conditions gracefully according to their specified contract (e.g., returning `None`, an empty list, or a specific error object) rather than propagating raw exceptions, unless the contract explicitly states otherwise.
- refined_io_mocking_strategy: When testing I/O operations, carefully distinguish between mocking read and write operations. If `builtins.open` is mocked to simulate a read error, ensure that any setup (like creating the file) is done *before* the mock is applied, or use separate mocks/strategies for different I/O modes. For `mock_open`, apply `side_effect` to the *return value* of `open()` (the file handle) for read errors, not `open()` itself if you need to create the file first.
- enforce_single_cli_exit_point: Design the `main` function of a CLI tool to have a clear, single point of exit (or a minimal set of well-defined exit points) to ensure predictable behavior and testability. Use `return` statements or `sys.exit()` strategically to prevent further execution after an error.
- precise_cli_output_mocking: When testing CLI tools, ensure `sys.argv` is mocked with actual string values, not mock objects, to prevent `MagicMock` references in error messages. Assertions on `sys.stderr` should target specific, isolated error messages, not combined or unexpected output.
- immediate_exit_on_validation_failure: After detecting invalid command-line arguments, a CLI tool must print an error message and immediately call `sys.exit(1)` to prevent any further execution of the core logic, avoiding `IndexError` or other unexpected behavior.
- consistent_core_logic_return: A utility function designed to provide data for CLI output (e.g., JSON) should consistently return a structured data type (e.g., a dictionary, even if empty) on success, rather than `None`, to ensure predictable serialization.
- comment_non_code_text: Always use the language's appropriate comment syntax for any non-code text, instructions, or prompts within source code files.
- phase_scope_adherence: Always strictly adhere to the defined scope for the current development phase, focusing solely on the required deliverables and deferring all out-of-scope features to subsequent phases.
- <rule_name_snake_case>: <rule_description>
- direct_simple_task_execution: For simple, direct tasks, execute them precisely as instructed without over-engineering or misinterpretation, ensuring exact adherence to specified file paths and content.
- design_and_test_first: Always design the architecture and write comprehensive test cases before implementing the core logic, especially for new features or components, to ensure correctness and prevent early failures.
- robust_data_persistence: Always ensure data persistence layers (e.g., storage.py) handle serialization/deserialization of custom objects correctly and gracefully manage file system errors (e.g., `FileNotFoundError`) by returning sensible defaults as per requirements.
- avoid_sys_exit_directly: Avoid using sys.exit() directly in main functions
- calculate_rule: <calculate_rule_snake_case> | This function takes three arguments and performs arithmetic operations based on user input.
- consistent_naming_convention: Use a consistent naming convention for variables and functions.
- initialize_game_state_correctly: Always verify the successful completion and correctness of a prerequisite step before starting a dependent step.
- check_win: <check_win_snake_case> | Checks all 8 winning combinations (3 rows, 3 columns, 2 diagonals) to determine if the specified player has won.
- check_draw_rule: Checks if all 9 spots on the board are filled
- separation_of_concerns_for_business_logic: Business logic (e.g., state validation, record creation) must be encapsulated in dedicated modules (e.g., `data_manager.py`) and should not directly handle I/O operations or CLI argument parsing.
- cli_entry_point_structure: The main entry point script (e.g., main.py) must strictly handle argument parsing, validation, and user I/O, while delegating all core business logic to a dedicated, modular service layer (e.g., data_manager.py).
- correct_multi_line_string_termination: Always ensure multi-line string literals, especially f-strings, are correctly terminated with matching triple quotes (""") to prevent `SyntaxError: unterminated triple-quoted f-string literal`.


### 🔍 過去の記録からの抜粋
- [Failure Pattern] Failing to achieve a fully functional and error-free multi-module application on the first attempt due to issues like incorrect module implementation, broken dependencies, or integration errors. -> [Success Snippet] Successfully implementing all specified modules (`models.py`, `storage.py`, `cli.py`) with precise adherence to requirements, ensuring correct inter-module dependencies and seamless integration, resulting in a perfectly functional application from the initial execution.
- [Failure Pattern] Introducing regressions or failing to meet all specified conditions when extending an existing API with new features -> [Success Snippet] Successfully extended the Todo API by implementing update (PUT /todos/{task_id}) and delete (DELETE /todos/{task_id}) functionalities, meticulously preserving all existing endpoints (/health, POST /todos, GET /todos), strictly adhering to in-memory data storage, and correctly utilizing FastAPI's routing and Pydantic models, demonstrating comprehensive requirement adherence and regression prevention.
- [Failure Pattern] Deviating from specified implementation details (e.g., data storage, data models, or API endpoint scope) -> [Success Snippet] Strictly adhere to all specified requirements, including the designated data storage mechanism (e.g., in-memory list), the required data model definition (e.g., Pydantic), and the exact set of API endpoints and features for the current development phase, while preserving existing functionality.



【Current Task: Single Pass Mode】
【ミッション: 独立品質監査API「The Pharos」の建造】

# Goal
FastAPIを用いて、与えられたコード（GitHubリポジトリURL、またはGit Diff）の品質を静的解析とLLMを用いて評価し、スコア化する独立したAPIサーバー「The Pharos」を構築してください。

# System Requirements
## 1. 概要
- フレームワーク: FastAPI
- 言語: Python 3.11+
- レスポンス: 「セキュリティ」「保守性」「パフォーマンス」を100点満点で評価したJSON。

## 2. ディレクトリ構成（モジュラーアーキテクチャ）
以下の構成で実装を分割してください。
project_root/
├── main.py
├── api/
│   └── routes.py
├── models/
│   └── schemas.py
├── services/
│   ├── github.py
│   ├── analyzer.py
│   └── llm_reviewer.py
└── core/
    └── config.py

※ `core/config.py` では `pydantic-settings` を用いて、環境変数（LLMのAPIキーなど）を安全に読み込む設計にしてください。

## 3. Pydantic Models (models/schemas.py)
必ず以下のスキーマを使用してレスポンスを生成してください。

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ReviewRequest(BaseModel):
    github_url: Optional[str] = Field(None, description="GitHub Repository URL")
    diff_content: Optional[str] = Field(None, description="Raw Git Diff string")

class CategoryScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Score out of 100")
    issues: List[str] = Field(..., description="List of identified issues")
    suggestions: List[str] = Field(..., description="Actionable improvement suggestions")

class ReviewResponse(BaseModel):
    security: CategoryScore
    maintainability: CategoryScore
    performance: CategoryScore
    overall_summary: str = Field(..., description="Brief overall evaluation summary")
```

## 4. エンドポイント仕様
- `POST /api/v1/review`
  - 入力: `ReviewRequest`
  - 出力: `ReviewResponse`
  - 挙動: `github_url`と`diff_content`のどちらか一方が提供されること。両方空の場合は400エラー。処理は同期的に行い、静的解析（今回はダミーのランダムスコア減点ロジックでも可）とLLMのレビュー結果をマージしてJSONを返す。

## 5. LLMの統合 (services/llm_reviewer.py)
- `litellm` パッケージを使用してLLM（例: `gpt-4o` や `gemini-2.5-flash` など任意）を呼び出してください。
- 出力フォーマットを厳密に守らせるため、Pydanticモデルを利用した Structured Outputs（構造化出力）機能を用いて、確実に `ReviewResponse` スキーマに合致するJSONを返却させてください。

## 6. アーキテクチャ・制約事項
- モジュールの結合度を下げるため、`api/routes.py` にはビジネスロジックを書かず、`services/` 配下の関数を呼び出すだけにしてください。
- 外部API（GitHubやLLM）の呼び出し部分には適切な例外処理（try-except）とHTTPエラー（`HTTPException`）の送出を含めてください。

# Execution
上記の要件を満たすPythonコード一式（要件を網羅する各ファイルの内容）を出力してください。


### 📌 現在適用されているコアルール
- verify_prerequisites: Always verify the successful completion and correctness of a prerequisite step before starting a dependent step.
- simple_execution_instructions: For basic tasks, provide the simplest, most direct, and universally applicable execution instructions.
- holistic_review: When creating or modifying interdependent artifacts, perform a final holistic review or simulated execution to ensure all parts work together and instructions accurately reflect the current state.
- cli_argument_adherence: Always provide all required command-line arguments when executing a CLI tool, as indicated by its `usage` message or error output.
- verify_executable_path_and_installation: Before attempting to execute any program or script, especially those within a virtual environment or specific path, verify that the executable exists at the specified path and is correctly installed/accessible within the current environment.
- diagnose_errors_before_retry: When an execution fails with an error message, always pause and diagnose the root cause of the error before attempting to retry the same or a similar command. Do not blindly repeat failed commands.
- single_exit_point_cli: A CLI tool's `main` function should have a single, clear exit point or ensure that `sys.exit()` is called exactly once per execution path (success or specific error).
- robust_cli_argument_validation: Always validate command-line arguments at the very beginning of the `main` function of a CLI tool. Check for the correct number of arguments and their types/existence before proceeding with core logic.
- single_valid_json_output: When a CLI tool is designed to output JSON, ensure that the entire standard output stream contains *only* a single, valid JSON object or array, and nothing else (no extra newlines, debug prints, or multiple JSON objects concatenated).
- utility_function_error_contract: Utility functions should handle expected error conditions gracefully according to their specified contract (e.g., returning `None`, an empty list, or a specific error object) rather than propagating raw exceptions, unless the contract explicitly states otherwise.
- refined_io_mocking_strategy: When testing I/O operations, carefully distinguish between mocking read and write operations. If `builtins.open` is mocked to simulate a read error, ensure that any setup (like creating the file) is done *before* the mock is applied, or use separate mocks/strategies for different I/O modes. For `mock_open`, apply `side_effect` to the *return value* of `open()` (the file handle) for read errors, not `open()` itself if you need to create the file first.
- enforce_single_cli_exit_point: Design the `main` function of a CLI tool to have a clear, single point of exit (or a minimal set of well-defined exit points) to ensure predictable behavior and testability. Use `return` statements or `sys.exit()` strategically to prevent further execution after an error.
- precise_cli_output_mocking: When testing CLI tools, ensure `sys.argv` is mocked with actual string values, not mock objects, to prevent `MagicMock` references in error messages. Assertions on `sys.stderr` should target specific, isolated error messages, not combined or unexpected output.
- immediate_exit_on_validation_failure: After detecting invalid command-line arguments, a CLI tool must print an error message and immediately call `sys.exit(1)` to prevent any further execution of the core logic, avoiding `IndexError` or other unexpected behavior.
- consistent_core_logic_return: A utility function designed to provide data for CLI output (e.g., JSON) should consistently return a structured data type (e.g., a dictionary, even if empty) on success, rather than `None`, to ensure predictable serialization.
- comment_non_code_text: Always use the language's appropriate comment syntax for any non-code text, instructions, or prompts within source code files.
- phase_scope_adherence: Always strictly adhere to the defined scope for the current development phase, focusing solely on the required deliverables and deferring all out-of-scope features to subsequent phases.
- <rule_name_snake_case>: <rule_description>
- direct_simple_task_execution: For simple, direct tasks, execute them precisely as instructed without over-engineering or misinterpretation, ensuring exact adherence to specified file paths and content.
- design_and_test_first: Always design the architecture and write comprehensive test cases before implementing the core logic, especially for new features or components, to ensure correctness and prevent early failures.
- robust_data_persistence: Always ensure data persistence layers (e.g., storage.py) handle serialization/deserialization of custom objects correctly and gracefully manage file system errors (e.g., `FileNotFoundError`) by returning sensible defaults as per requirements.
- avoid_sys_exit_directly: Avoid using sys.exit() directly in main functions
- calculate_rule: <calculate_rule_snake_case> | This function takes three arguments and performs arithmetic operations based on user input.
- consistent_naming_convention: Use a consistent naming convention for variables and functions.
- initialize_game_state_correctly: Always verify the successful completion and correctness of a prerequisite step before starting a dependent step.
- check_win: <check_win_snake_case> | Checks all 8 winning combinations (3 rows, 3 columns, 2 diagonals) to determine if the specified player has won.
- check_draw_rule: Checks if all 9 spots on the board are filled
- separation_of_concerns_for_business_logic: Business logic (e.g., state validation, record creation) must be encapsulated in dedicated modules (e.g., `data_manager.py`) and should not directly handle I/O operations or CLI argument parsing.
- cli_entry_point_structure: The main entry point script (e.g., main.py) must strictly handle argument parsing, validation, and user I/O, while delegating all core business logic to a dedicated, modular service layer (e.g., data_manager.py).
- correct_multi_line_string_termination: Always ensure multi-line string literals, especially f-strings, are correctly terminated with matching triple quotes (""") to prevent `SyntaxError: unterminated triple-quoted f-string literal`.


### 🔍 過去の記録からの抜粋
- [Failure Pattern] Failing to achieve a fully functional and error-free multi-module application on the first attempt due to issues like incorrect module implementation, broken dependencies, or integration errors. -> [Success Snippet] Successfully implementing all specified modules (`models.py`, `storage.py`, `cli.py`) with precise adherence to requirements, ensuring correct inter-module dependencies and seamless integration, resulting in a perfectly functional application from the initial execution.
- [Failure Pattern] Introducing regressions or failing to meet all specified conditions when extending an existing API with new features -> [Success Snippet] Successfully extended the Todo API by implementing update (PUT /todos/{task_id}) and delete (DELETE /todos/{task_id}) functionalities, meticulously preserving all existing endpoints (/health, POST /todos, GET /todos), strictly adhering to in-memory data storage, and correctly utilizing FastAPI's routing and Pydantic models, demonstrating comprehensive requirement adherence and regression prevention.
- [Failure Pattern] Deviating from specified implementation details (e.g., data storage, data models, or API endpoint scope) -> [Success Snippet] Strictly adhere to all specified requirements, including the designated data storage mechanism (e.g., in-memory list), the required data model definition (e.g., Pydantic), and the exact set of API endpoints and features for the current development phase, while preserving existing functionality.



            if __name__ == "__main__":
                print("解析に失敗したみたい。もう一度具体的な指示をちょうだい💋")
