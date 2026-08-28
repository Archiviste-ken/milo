from groq import Groq

from app.prompts import SYSTEM_PROMPT
from app.tools.registry import (
    TOOL_DEFINITIONS,
    execute_tool,
)


class GroqClient:

    def __init__(
        self,
        api_key: str,
        model: str,
        max_iterations: int = 5,
    ):
        self.client = Groq(
            api_key=api_key
        )

        self.model = model
        self.max_iterations = max_iterations

        self.messages: list[dict] = []

    def chat(self, user_input: str) -> str:

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        for _ in range(self.max_iterations):

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    *self.messages,
                ],
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            message = response.choices[0].message

            self.messages.append(message)

            if not message.tool_calls:
                assistant_message = (
                    message.content or ""
                )

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message,
                    }
                )

                return assistant_message

            for tool_call in message.tool_calls:

                tool_name = (
                    tool_call.function.name
                )

                tool_arguments = (
                    tool_call.function.arguments
                )

                print(
                    f"\n🔧 Tool requested: {tool_name}"
                )

                result = execute_tool(
                    tool_name,
                    tool_arguments,
                )

                print(
                    f"📦 Tool result: {result}"
                )

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": str(result),
                    }
                )

        return (
            "I stopped because the maximum "
            "number of tool iterations was reached."
        )