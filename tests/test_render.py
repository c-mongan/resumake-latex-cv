from pathlib import Path

import pytest

from resumake_cv.render import latex_escape, load_cv, render_latex


ROOT = Path(__file__).resolve().parents[1]


def test_latex_escape_handles_reserved_characters() -> None:
    assert latex_escape("R&D_100%") == r"R\&D\_100\%"


def test_sample_renders_expected_sections() -> None:
    data = load_cv(ROOT / "examples" / "sample-cv.json")
    rendered = render_latex(data)
    assert "Jordan Lee" in rendered
    assert r"\resumeheader{Work Experience}" in rendered
    assert r"\resumeheader{Selected Projects}" in rendered
    assert r"30 percent" in rendered
    assert "Python, SQL, PostgreSQL" in rendered
    assert "built-in method" not in rendered


def test_missing_name_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "invalid.json"
    source.write_text('{"skills": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="name"):
        load_cv(source)
