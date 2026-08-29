import json

from app.agent.state import AgentState
from app.agent.verifier import verify_tool_result
from app.agent.planner import Planner
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

        self.planner = Planner(llm)

        self.state = AgentState()

    def run(self, user_input: str) -> str:

        self.state = AgentState(
            status="running"
        )

        # ---------------------------------
        # 1. Create an LLM-generated plan
        # ---------------------------------

        plan = self.planner.create_plan(
            user_input
        )

        self.state.plan = [
            step.action
            for step in plan.steps
        ]

        print("\n📋 MILO PLAN")
        print(f"🎯 Goal: {plan.goal}")

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            print(
                f"  {index}. "
                f"{step.action} "
                f"{step.arguments}"
            )

        # ---------------------------------
        # 2. Add user message to state
        # ---------------------------------

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

        # ---------------------------------
        # 3. Agent execution loop
        # ---------------------------------

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

            # ---------------------------------
            # 4. No tool call → final answer
            # ---------------------------------

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

            # ---------------------------------
            # 5. Store assistant tool request
            # ---------------------------------

            self.state.messages.append(
                message
            )

            # ---------------------------------
            # 6. Execute requested tools
            # ---------------------------------

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

                # Execute
                result = execute_tool(
                    name,
                    arguments,
                )

                result_dict = result.to_dict()

                # ---------------------------------
                # 7. Store observation
                # ---------------------------------

                self.state.observations.append(
                    {
                        "tool": name,
                        "result": result_dict,
                    }
                )

                # ---------------------------------
                # 8. Verify result
                # ---------------------------------

                verification = verify_tool_result(
                    name,
                    result,
                )

                self.state.verifications.append(
                    {
                        "tool": name,
                        "verification": verification,
                    }
                )

                print(
                    f"📦 Result: {result_dict}"
                )

                print(
                    f"🔍 Verification: {verification}"
                )

                # ---------------------------------
                # 9. Send observation back to LLM
                # ---------------------------------

                self.state.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": json.dumps(
                            result_dict
                        ),
                    }
                )

        # ---------------------------------
        # 10. Iteration limit reached
        # ---------------------------------

        self.state.status = "max_iterations"

        return (
            "I stopped because the agent "
            "reached its iteration limit."
        )