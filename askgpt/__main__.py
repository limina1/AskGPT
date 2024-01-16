"""askgpt entry script"""
# askgpt/__main__.py

from askgpt import cli, __app_name__, askgpt


def main():
    cli.app(prog_name=__app_name__)
    cli.main()

if __name__ == '__main__':
    main()
