from app.agent.state import AgentState
from app.agent.planner import Planner
from app.agent.executor import PlanExecutor
from app.prompts import SYSTEM_PROMPT


class Agent:

    def __init__(
        self,
        llm,
        max_iterations: int = 5,
    ):
        self.llm = llm
        self.max_iterations = max_iterations

        self.planner = Planner(llm)
        self.executor = PlanExecutor()

        self.state = AgentState()

    def run(self, user_input: str) -> str:

        self.state = AgentState(
            status="running"
        )

        # ---------------------------------
        # 1. CREATE PLAN
        # ---------------------------------

        plan = self.planner.create_plan(
            user_input
        )

        self.state.plan = plan.steps

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
        # 2. EXECUTE PLAN
        # ---------------------------------

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):

            self.state.current_step = index

            print(
                f"\n⚙️ Step {index}/{len(plan.steps)}"
            )

            result, verification = (
                self.executor.execute_step(
                    step
                )
            )

            # ---------------------------------
            # 3. RECORD TOOL CALL
            # ---------------------------------

            self.state.tool_calls.append(
                {
                    "name": step.action,
                    "arguments": step.arguments,
                }
            )

            # ---------------------------------
            # 4. RECORD OBSERVATION
            # ---------------------------------

            result_dict = result.to_dict()

            self.state.observations.append(
                {
                    "tool": step.action,
                    "result": result_dict,
                }
            )

            # ---------------------------------
            # 5. RECORD VERIFICATION
            # ---------------------------------

            self.state.verifications.append(
                {
                    "tool": step.action,
                    "verification": verification,
                }
            )

            # ---------------------------------
            # 6. STOP IF TOOL FAILED
            # ---------------------------------

            if not verification.get(
                "verified",
                False,
            ):

                self.state.status = "failed"

                return (
                    f"MILO could not complete "
                    f"step {index}: "
                    f"{step.action}"
                )

        # ---------------------------------
        # 7. GENERATE FINAL RESPONSE
        # ---------------------------------

        self.state.status = "completed"

        response = self.llm.chat(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
                {
                    "role": "system",
                    "content": (
                        "The requested task has been "
                        "executed successfully.\n\n"
                        f"Goal: {plan.goal}\n\n"
                        "Execution results:\n"
                        f"{self.state.observations}"
                    ),
                },
            ]
        )

        return (
            response.choices[0]
            .message
            .content
            or ""
        )