# tests/test_askgpt.py

from typer.testing import CliRunner

from askgpt import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0
    assert result.stdout == f'{__app_name__} version {__version__}\n' in result.stdout
