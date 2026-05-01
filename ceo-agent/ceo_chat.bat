@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "MODEL=qwen3.5:0.8b"

if "%~1"=="" (
  set "MSG=Plan this week for Magna Conscius and prioritize first supermarket pilot."
) else (
  set "MSG=%*"
)

python "%SCRIPT_DIR%chat_ceo.py" --provider ollama --ollama-model %MODEL% --message "%MSG%"

endlocal

