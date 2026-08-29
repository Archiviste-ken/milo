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

    if not plan.steps:
        raise ValueError(
            "Plan must contain at least one step."
        )

    for step in plan.steps:

        if step.action not in ALLOWED_ACTIONS:
            raise ValueError(
                f"Action not allowed: "
                f"{step.action}"
            )