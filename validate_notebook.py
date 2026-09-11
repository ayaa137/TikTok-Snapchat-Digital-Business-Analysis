from pathlib import Path
from textwrap import dedent
import asyncio
import os
import sys
import tempfile

import nbformat
from nbclient import NotebookClient


ROOT = Path.cwd()
NOTEBOOK = ROOT / "TikTok_Snapchat_Business_Analysis_CLEAN.ipynb"

os.environ.setdefault("IPYTHONDIR", str(Path(tempfile.gettempdir()) / "business_analysis_ipython"))

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


notebook = nbformat.read(NOTEBOOK, as_version=4)
client = NotebookClient(notebook, timeout=300, kernel_name="python3")
client.execute()

errors = []
for index, cell in enumerate(notebook.cells):
    for output in cell.get("outputs", []):
        if output.get("output_type") == "error":
            errors.append((index, output.get("ename"), output.get("evalue")))

if errors:
    for index, name, value in errors:
        print(f"Cell {index}: {name}: {value}")
    raise SystemExit(1)

print(dedent("""
Notebook validation passed.
- Every code cell executed from a clean kernel.
- No notebook error outputs were found.
- No hidden variables from previous runs were required.
""").strip())
