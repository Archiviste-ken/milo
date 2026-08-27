from groq import Groq

from app.prompts import SYSTEM_PROMPT


class GroqClient:

    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def chat(self, messages: list[dict]) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *messages,
            ],
        )

        return response.choices[0].message.content