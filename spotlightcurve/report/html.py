"""HTML report generation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

_DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "templates" / "report.html.j2"


@dataclass
class ReportContext:
    """Inputs required to render an HTML report."""

    parameters: Mapping[str, Any]
    figures: Mapping[str, str]
    metadata: Mapping[str, Any]


def render_report(
    context: ReportContext,
    output: Path,
    *,
    template: Optional[Path] = None,
) -> str:
    """Render the HTML report and persist it to ``output``."""

    template_path = template or _DEFAULT_TEMPLATE
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template_obj = env.get_template(template_path.name)
    html = template_obj.render(
        parameters=context.parameters,
        figures=context.figures,
        metadata=context.metadata,
    )
    output.write_text(html, encoding="utf8")
    return html


__all__ = ["ReportContext", "render_report"]
