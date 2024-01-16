# askgpt/askgpt.py
import openai
import os
import typer

class AskGPT:
    def __init__(self, custom_prompt=None, model_id=None):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.chat = openai.chat.completions
        if custom_prompt or model_id:
            custom = []
            if custom_prompt:
                custom.append(f"model: {model_id}")
                self.conversation = [
                    {"role": "system", "content": custom_prompt},
                ]
            if model_id:
                custom.append(f"prompt: {custom_prompt}")
                self.model_id = model_id
            for line in custom:
                print(f"Using custom {line}")
        if not custom_prompt:
            self.conversation = [
                {"role": "system", "content": "You are an informative cli assistant providing technical support to a user. Please answer their query in a minimal, concise manner"},
            ]
        if not model_id:
            self.model_id = "gpt-3.5-turbo-1106"
        self.respose = None

    def ask(self, question, append=True):
        self.conversation.append({"role": "user", "content": question})
        response = self.chat.create(model=self.model_id,
                                    messages=self.conversation,
                                          )
        self.answer = response.choices[0].message.content
        if append:
            self.conversation.append({'role': 'system', 'content': self.answer})
        typer.echo(self.answer, err=True)
        return self.answer

    def save(self):
        print("Saving conversation...")
        self.ask("Please provide a name for this conversation.")
        self.answer = self.answer.replace(" ", "_")
        # replace quotes with nothing
        self.answer = self.answer.replace("\"", "")
        self.answer = self.answer.replace("\'", "")
        print("conversation saved as: ", self.answer+".txt")
        with open(f"{self.answer}.txt", "w") as f:
            for message in self.conversation:
                f.write(f"{message['role']}: {message['content']}\n")
