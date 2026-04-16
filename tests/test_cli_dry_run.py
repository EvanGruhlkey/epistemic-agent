from __future__ import annotations

from epistemic.cli import main


def test_cli_dry_run_transparent_succeeds() -> None:
    assert main(["--dry-run", "-m", "hello", "--mode", "transparent"]) == 0


def test_cli_dry_run_prints_gated_content(capsys) -> None:
    main(["--dry-run", "-m", "hello", "--mode", "transparent"])
    out = capsys.readouterr().out
    assert "reproduced here as given" in out or "inferred" in out.lower()
