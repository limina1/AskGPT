from typing import Optional
import typer
import sys
import fileinput
import select
import os
from askgpt import __app_name__, __version__, askgpt

app = typer.Typer()

def __version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} version {__version__}')
        raise typer.Exit()

def read_from_stdin():
    if select.select([sys.stdin,],[],[],0.0)[0]:
        stdin = sys.stdin.read().strip()
        stdin+="\n"
        return stdin
    else:
        return ""

@app.callback()
def init(
    version: Optional[bool] = typer.Option(
        None,
        '--version',
        '-v',
        help='Show version and exit.',
        callback=__version_callback,
        is_eager=True,
    ),
) -> None:
    return

@app.command()
def main(
    question: str = typer.Argument(None, help='Question to ask GPT-4.'),
    # priority: int = typer.Option(2, '--priority', '-p', min=1, max=3),
    chat: bool = typer.Option(False, '--chat', '-c',
                              help='Chat loop with GPT-4. \nType "exit" to exit or "save" to save conversation.'),
    # model: bool = typer.Option(False, '--model_id {model_id}', '-m {model_id}}',
                               # help='Specify an OpenAI model to use.\nhttps://platform.openai.com/docs/models'),
    prompt: str = typer.Option(None, '--custom_prompt', "-p", '{custom_prompt}', help='Specify a custom prompt to use.'),
    model: str = typer.Option(None, '--model_id', '-m', "{model_id}", help='Specify an OpenAI model to use.\nhttps://platform.openai.com/docs/models')

) -> str:
    """Ask a question to GPT-4."""
    convo = askgpt.AskGPT()
    if model:
        convo.model_id = model
        print(f"Using model: {model}")
    if prompt:
        convo.conversation = [
            {"role": "system", "content": prompt},
        ]
        print(f"Using custom prompt: {prompt}")
    if model or prompt:
        print("------------------")
    stdin = read_from_stdin()
    question = stdin + question
    # typer.echo(f"asking: {question}", err=True)
    convo.ask(question)
    if chat:
        # print("chatting with chatgpt")
        while True:
            question = input("user: ")
            if question == "":
                continue
            if question == "save":
                convo.save()
                question = 'exit'
            if question == "exit":
                break
            convo.ask(question)

typer.run(main)
