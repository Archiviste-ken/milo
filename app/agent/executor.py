import json

from app.agent.verifier import verify_tool_result
from app.tools.registry import execute_tool


class PlanExecutor:

    def execute_step(self, step):

        print(
            f"\n⚙️ Executing: {step.action}"
        )

        result = execute_tool(
            step.action,
            json.dumps(step.arguments),
        )

        result_dict = result.to_dict()

        verification = verify_tool_result(
            step.action,
            result,
        )

        print(
            f"📦 Result: {result_dict}"
        )

        print(
            f"🔍 Verification: {verification}"
        )

        return result, verification