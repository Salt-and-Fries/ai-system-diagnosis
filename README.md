# ai-system-diagnoser

Local-first assistant that inspects your machine, summarizes likely issues, and optionally proposes fixes. The initial target is Windows 10/11, but most read-only diagnostics also run on Linux/macOS.

## Features
- Interactive CLI that can call diagnostic tools (system overview, processes, disk health, event logs, network).
- Optional fix operations (restart service, run `sfc /scannow`, disable startup item stub) gated by a confirmation prompt.
- Structured tool schemas for OpenAI tool calling.
- Logging to `ai-system-diagnoser.log` so tool executions are recorded.

## Getting started
1. Install dependencies (Python 3.10+):
   ```bash
   pip install .[development]
   ```

   For the Tkinter UI (requires system Tk display support):
   ```bash
   pip install .[ui]
   ```
   If Tk or the HTML widget can't start (e.g., no display, missing `tkhtmlview`, or platform-specific Pillow wheels), the app will
   automatically fall back to the CLI and print the reason.
2. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY` and any overrides.
3. Run in diagnostic-only mode (default):
   ```bash
   python -m src.main
   ```
   or allow fixes:
   ```bash
   python -m src.main --allow-fixes
   ```
4. Type your issue description and follow the prompts. Type `exit` to quit.

## Tests
Run the lightweight smoke tests:
```bash
pytest
```
