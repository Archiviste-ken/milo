from app.tools.registry import execute_tool
from app.agent.verifier import verify_tool_result


class PlanExecutor:

    def execute_step(
        self,
        step,
    ):

        print(
            f"\n⚙️ Executing: {step.action}"
        )

        result = execute_tool(
            step.action,
            __import__("json").dumps(
                step.arguments
            ),
        )

        verification = verify_tool_result(
            step.action,
            result,
        )

        print(
            f"📦 Result: {result.to_dict()}"
        )

        print(
            f"🔍 Verification: {verification}"
        )

        return result, verification