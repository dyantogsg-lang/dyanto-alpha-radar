from __future__ import annotations

import asyncio
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown

from dyanto_alpha_radar.analyzer import analyze
from dyanto_alpha_radar.report import render_markdown_report

app = typer.Typer(help="Dyanto AlphaRadar — autonomous crypto market intelligence agent")
console = Console()


@app.command()
def scan(
    target: str = typer.Argument(..., help="Token address, pair, symbol, or search query"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Save markdown report path"),
    json_out: bool = typer.Option(False, "--json", help="Print raw JSON analysis"),
):
    """Scan one token/query and render an intelligence report."""
    result = asyncio.run(analyze(target))
    if json_out:
        console.print_json(json.dumps(result, indent=2))
        return
    report = render_markdown_report(result) if "error" not in result else json.dumps(result, indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        console.print(f"Saved: {output}")
    console.print(Markdown(report))


if __name__ == "__main__":
    app()
