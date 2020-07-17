"""
Tests for `startproject` command.
"""
import os
import subprocess
from textx.cli import textx
from click.testing import CliRunner

this_folder = os.path.abspath(os.path.dirname(__file__))


def test_startproject_smoke():
    """
    Basic smoke test that `startproject` can be invoked without errors.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['startproject'])
    # assert result.exit_code == 0
    assert 'Usage: textx startproject [OPTIONS] OUTPUT_PATH' in result.output


def test_startproject_language():
    """
    Basic test for generating of language project.
    """

    project_root = os.path.join(os.path.dirname(__file__), 'langprojecttest')

    p = subprocess.Popen([
        'textx', 'startproject', '--overwrite', project_root
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = p.communicate(input='1\n*.test\nmylang\nmylangpackage\nIgor Dejanovic\nmyemail@somewhere.com\nThis is a short description\n'.encode('utf-8'))  # noqa
    assert 'mylangpackage/mylang.tx\nDone.' in output[0].decode('utf-8')
    assert os.path.exists(project_root)
    assert os.path.exists(os.path.join(project_root,
                                       'mylangpackage',
                                       'mylang.tx'))
    with open(os.path.join(project_root, 'CHANGELOG.md'), 'r') as f:
        content = f.read()

    assert '# langprojecttest changelog' in content


def test_startproject_generator():
    """
    Basic test for generating of generator project.
    """

    project_root = os.path.join(os.path.dirname(__file__), 'genprojecttest')

    p = subprocess.Popen([
        'textx', 'startproject', '--overwrite', project_root
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = p.communicate(input='2\nnmygen\njinja2\nmygenpackage\nIgor Dejanovic\nmyemail@somewhere.com\nThis is a short description\n'.encode('utf-8'))  # noqa
    assert 'genprojecttest/mygenpackage/__init__.py\nDone.' in output[0].decode('utf-8')
    assert os.path.exists(project_root)
    assert os.path.exists(os.path.join(project_root, 'CHANGELOG.md'))
    with open(os.path.join(project_root,
                           'mygenpackage',
                           '__init__.py'), 'r') as f:
        content = f.read()

    assert "@generator('nmygen', 'jinja2')" in content
