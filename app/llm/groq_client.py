from groq import Groq

from app.prompts import SYSTEM_PROMPT


class GroqClient:

    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

        self.messages: list[dict] = []

    def chat(self, user_input: str) -> str:

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *self.messages,
            ],
        )

        assistant_message = (
            response.choices[0].message.content
            or ""
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

        return assistant_message