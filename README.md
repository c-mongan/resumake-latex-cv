# Resumake LaTeX CV

Generate a compact, one-page, ATS-friendly CV from structured JSON. The output
uses a classic Resumake-style layout: serif typography, simple section rules,
right-aligned dates and locations, and no decorative graphics or columns that
can confuse applicant-tracking systems.

The committed example is entirely fictional. Keep real CV data in an ignored
file or outside the repository.

## Requirements

- Python 3.10+
- `pdflatex` from TeX Live, MacTeX or MiKTeX when building a PDF

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Generate a CV

Create LaTeX only:

```bash
resumake-cv examples/sample-cv.json --tex build/sample-cv.tex
```

Create LaTeX and PDF:

```bash
resumake-cv examples/sample-cv.json \
  --tex build/sample-cv.tex \
  --pdf build/sample-cv.pdf
```

The input schema is demonstrated in
[`examples/sample-cv.json`](examples/sample-cv.json). Empty sections are
omitted. Contact entries accept optional `label`, `value` and `url` fields.

## Privacy

- Do not commit a real CV or generated PDF containing personal information.
- Store private inputs outside the repository, or use a filename covered by
  `.gitignore`.
- Review `git diff --cached` before every commit.
- The repository's tests verify that its fictional sample renders correctly;
  they do not validate the truth of user-supplied claims.

## Test

```bash
python -m pytest
```

## License

MIT
