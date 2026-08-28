from app.prompts import SYSTEM_PROMPT
from app.tools.registry import (
    TOOL_DEFINITIONS,
    execute_tool,
)


class Agent:

    def __init__(
        self,
        llm,
        max_iterations: int = 5,
    ):
        self.llm = llm
        self.max_iterations = max_iterations

        self.messages: list[dict] = []

    def run(self, user_input: str) -> str:

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }

        for iteration in range(
            self.max_iterations
        ):

            response = self.llm.chat(
                messages=[
                    system_message,
                    *self.messages,
                ],
                tools=TOOL_DEFINITIONS,
            )

            message = response.choices[0].message

            if not message.tool_calls:

                content = (
                    message.content or ""
                )

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                    }
                )

                return content

            self.messages.append(message)

            for tool_call in message.tool_calls:

                name = tool_call.function.name

                arguments = (
                    tool_call.function.arguments
                )

                print(
                    f"\n🔧 Tool: {name}"
                )

                result = execute_tool(
                    name,
                    arguments,
                )

                print(
                    f"📦 Result: {result}"
                )

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": str(result),
                    }
                )

        return (
            "I stopped because the agent "
            "reached its iteration limit."
        )