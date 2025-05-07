"""
Tests for `startproject` command.
"""
import os
import sys

import pexpect
from click.testing import CliRunner
from textx.cli import textx

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

    child = pexpect.spawn('textx startproject --overwrite ' + project_root)
    child.logfile = sys.stdout.buffer

    try:
        # Step through each prompt
        child.expect('Project type')
        child.sendline('1')  # Select language project

        child.expect('Language ID.*')
        child.sendline('mylang')

        child.expect('File extension.*')
        child.sendline('*.test')

        child.expect('Package name.*')
        child.sendline('mylangpackage')

        child.expect('Author.*')
        child.sendline('Igor Dejanovic')

        child.expect('email.*')
        child.sendline('myemail@somewhere.com')

        child.expect('description.*')
        child.sendline('This is a short description')

        # Wait for completion
        child.expect(pexpect.EOF, timeout=10)

        # Verify outputs
        assert 'mylangpackage/mylang.tx' in child.before.decode('utf-8')
        assert os.path.exists(project_root)
        assert os.path.exists(os.path.join(project_root, 'mylangpackage', 'mylang.tx'))

        with open(os.path.join(project_root, 'CHANGELOG.md')) as f:
            assert '# langprojecttest changelog' in f.read()

    finally:
        if child.isalive():
            child.terminate()


def test_startproject_generator():
    """
    Basic test for generating of generator project.
    """

    project_root = os.path.join(os.path.dirname(__file__), 'genprojecttest')

    # Start process
    child = pexpect.spawn('textx startproject --overwrite ' + project_root)

    child.logfile = sys.stdout.buffer

    try:
        child.expect('Project type.*')
        child.sendline('2')  # Select generator project

        child.expect('File extension.*')
        child.sendline('test')

        child.expect('Generator for language.*')
        child.sendline('mylang')

        child.expect('Target platform.*')
        child.sendline('jinja2')

        child.expect('Package name.*')
        child.sendline('mygenpackage')

        child.expect('Author.*')
        child.sendline('Igor Dejanovic')

        child.expect('email.*')
        child.sendline('myemail@somewhere.com')

        child.expect('description.*')
        child.sendline('This is a short description')

        child.expect(pexpect.EOF, timeout=10)

        assert 'genprojecttest/mygenpackage/__init__.py' in child.before.decode('utf-8')
        assert os.path.exists(project_root)
        assert os.path.exists(os.path.join(project_root, 'CHANGELOG.md'))

        with open(os.path.join(project_root, 'mygenpackage', '__init__.py')) as f:
            assert "@generator('mylang', 'jinja2')" in f.read()
            
    finally:
        if child.isalive():
            child.terminate()
