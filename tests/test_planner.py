from app.agent.planner import create_plan


plan = create_plan(
    "Remember that I'm learning AI and calculate 25 * 8."
)

for index, step in enumerate(plan, start=1):
    print(f"{index}. {step}")