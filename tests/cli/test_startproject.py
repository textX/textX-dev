"""
Tests for `startproject` command.
"""
import os
from textx.cli import textx
from click.testing import CliRunner

this_folder = os.path.abspath(os.path.dirname(__file__))


def test_startproject():
    """
    Basic smoke test that `startproject` can be invoked without errors.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['startproject'])
    # assert result.exit_code == 0
    assert 'Usage: textx startproject [OPTIONS] OUTPUT_PATH' in result.output
