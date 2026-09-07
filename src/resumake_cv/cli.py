from __future__ import annotations

import argparse
from pathlib import Path

from .render import build_pdf, load_cv, render_latex


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a Resumake-style LaTeX CV from JSON."
    )
    parser.add_argument("input", type=Path, help="Path to a UTF-8 JSON CV file")
    parser.add_argument(
        "--tex", type=Path, default=Path("build/cv.tex"), help="LaTeX output path"
    )
    parser.add_argument("--pdf", type=Path, help="Optional PDF output path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data = load_cv(args.input)
    latex = render_latex(data)
    args.tex.parent.mkdir(parents=True, exist_ok=True)
    args.tex.write_text(latex, encoding="utf-8")
    print(f"Wrote {args.tex}")

    if args.pdf:
        build_pdf(args.tex, args.pdf)
        print(f"Wrote {args.pdf}")


if __name__ == "__main__":
    main()
