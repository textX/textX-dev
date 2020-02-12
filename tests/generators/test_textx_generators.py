"""
Tests for textX registered generators/visualizations
"""
import os
import pytest
from textxdev.cli import textx
from click.testing import CliRunner


this_folder = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def metamodel_file():
    try:
        os.remove(os.path.join(this_folder, 'hello.pu'))
    except OSError:
        pass
    try:
        os.remove(os.path.join(this_folder, 'hello.dot'))
    except OSError:
        pass
    return os.path.join(this_folder, 'hello.tx')


def test_generate_dot_from_tx(metamodel_file):
    """
    Test generating dot from textX grammar.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['generate',
                                   '--target', 'dot',
                                   metamodel_file])
    assert result.exit_code == 0
    out_file = os.path.join(this_folder, 'hello.dot')
    assert os.path.exists(out_file)
    with open(out_file, 'r') as f:
        assert 'digraph textX' in f.read()


def test_generate_plantuml_from_tx(metamodel_file):
    """
    Test generating pu (PlantUML) file from textX grammar.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['generate',
                                   '--target', 'PlantUML',
                                   metamodel_file])
    assert result.exit_code == 0
    out_file = os.path.join(this_folder, 'hello.pu')
    assert os.path.exists(out_file)
    with open(out_file, 'r') as f:
        assert '@startuml' in f.read()


def test_generate_dot_from_any_model(metamodel_file):
    """
    Test generating dot from any textX model.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['generate',
                                   '--target', 'dot',
                                   '--grammar', metamodel_file,
                                   os.path.join(this_folder, 'example.hello')])

    assert result.exit_code == 0
    hello_file = os.path.join(this_folder, 'example.dot')
    assert os.path.exists(hello_file)
    with open(hello_file, 'r') as f:
        assert 'digraph textX' in f.read()
