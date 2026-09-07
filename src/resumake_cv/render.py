from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, StrictUndefined


LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(value: Any) -> str:
    """Escape plain input text for safe use in LaTeX."""
    text = "" if value is None else str(value)
    return "".join(LATEX_REPLACEMENTS.get(char, char) for char in text)


def load_cv(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("CV input must be a JSON object")
    if not data.get("name"):
        raise ValueError("CV input requires a non-empty 'name'")
    return data


def render_latex(data: dict[str, Any]) -> str:
    environment = Environment(
        loader=PackageLoader("resumake_cv", "templates"),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        comment_start_string=r"\COMMENT{",
        comment_end_string="}",
    )
    environment.filters["latex"] = latex_escape
    template = environment.get_template("resume.tex.j2")
    return template.render(cv=data)


def build_pdf(tex_path: Path, pdf_path: Path) -> None:
    pdflatex = shutil.which("pdflatex")
    if pdflatex is None:
        raise RuntimeError("pdflatex was not found; install TeX Live, MacTeX or MiKTeX")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="resumake_cv_") as temp_dir:
        command = [
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={temp_dir}",
            str(tex_path.resolve()),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"pdflatex failed:\n{result.stdout[-4000:]}")
        generated = Path(temp_dir) / f"{tex_path.stem}.pdf"
        if not generated.exists():
            raise RuntimeError("pdflatex completed without producing a PDF")
        shutil.copy2(generated, pdf_path)
