from app.agent.plan import Plan


ALLOWED_ACTIONS = {
    "calculate",
    "remember_memory",
    "recall_memory",
}


def validate_plan(plan: Plan) -> None:

    if not plan.goal.strip():
        raise ValueError(
            "Plan goal cannot be empty."
        )

    for step in plan.steps:

        if step.action not in ALLOWED_ACTIONS:
            raise ValueError(
                f"Action not allowed: "
                f"{step.action}"
            )