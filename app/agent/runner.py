from app.agent.state import AgentState
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

        self.state = AgentState()

    def run(self, user_input: str) -> str:

        self.state = AgentState(
            status="running"
        )

        self.state.messages.append(
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

            self.state.iteration = iteration + 1

            response = self.llm.chat(
                messages=[
                    system_message,
                    *self.state.messages,
                ],
                tools=TOOL_DEFINITIONS,
            )

            message = response.choices[0].message

            if not message.tool_calls:

                content = (
                    message.content or ""
                )

                self.state.messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                    }
                )

                self.state.status = "completed"

                return content

            self.state.messages.append(
                message
            )

            for tool_call in message.tool_calls:

                name = tool_call.function.name
                arguments = (
                    tool_call.function.arguments
                )

                self.state.tool_calls.append(
                    {
                        "name": name,
                        "arguments": arguments,
                    }
                )

                print(
                    f"\n🔧 Tool: {name}"
                )

                result = execute_tool(
                    name,
                    arguments,
                )

                self.state.observations.append(
                    {
                        "tool": name,
                        "result": result,
                    }
                )

                print(
                    f"📦 Result: {result}"
                )

                self.state.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": str(result),
                    }
                )

        self.state.status = "max_iterations"

        return (
            "I stopped because the agent "
            "reached its iteration limit."
        )