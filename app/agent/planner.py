import json

from app.agent.plan import Plan, PlanStep
from app.agent.plan_validator import (
    validate_plan,
)


PLANNER_PROMPT = """
You are the planning component of an AI agent.

Your job is to convert the user's request into
a small sequence of actions.

Available actions:

1. calculate
   arguments:
     expression: string

2. remember_memory
   arguments:
     fact: string

3. recall_memory
   arguments:
     query: string


IMPORTANT PLANNING RULES:

1. Only use the available actions.

2. Use the exact action names and argument names.

3. Never invent actions.

4. Do not perform the actions yourself.

5. Keep the plan as small as possible.

6. Use remember_memory ONLY when the user explicitly
   asks you to remember, save, store, or keep
   information for later.

7. Use recall_memory whenever the user's question
   requires information that may already exist in
   the agent's persistent memory.

8. Questions about the user's previously stored
   information REQUIRE recall_memory.

9. Examples of questions that require recall_memory:

   "What am I learning?"
   "What did I tell you about Python?"
   "What do you remember about me?"
   "What was the thing I asked you to remember?"

10. If the user asks a simple calculation,
    use calculate.

11. If the user explicitly asks to remember something,
    use remember_memory.

12. A plan with no steps should ONLY be used when
    the user's request genuinely requires no tool.

13. Do not create a step for simply producing the
    final response.


EXAMPLES:


User:
"What is 25 * 8?"

Plan:
{
    "goal": "Calculate the requested expression.",
    "steps": [
        {
            "action": "calculate",
            "arguments": {
                "expression": "25 * 8"
            }
        }
    ]
}


User:
"Remember that I am learning AI."

Plan:
{
    "goal": "Store the user's learning topic.",
    "steps": [
        {
            "action": "remember_memory",
            "arguments": {
                "fact": "User is learning AI."
            }
        }
    ]
}


User:
"What am I learning?"

Plan:
{
    "goal": "Retrieve the user's learning topic from memory.",
    "steps": [
        {
            "action": "recall_memory",
            "arguments": {
                "query": "What is the user learning?"
            }
        }
    ]
}


User:
"What do you remember about Python?"

Plan:
{
    "goal": "Retrieve relevant information about Python from memory.",
    "steps": [
        {
            "action": "recall_memory",
            "arguments": {
                "query": "What does the user remember or know about Python?"
            }
        }
    ]
}


Return ONLY valid JSON.

Format:

{
    "goal": "short description",
    "steps": [
        {
            "action": "action_name",
            "arguments": {}
        }
    ]
}
"""

class Planner:

    def __init__(self, llm):
        self.llm = llm

    def create_plan(
        self,
        user_input: str,
    ) -> Plan:

        response = self.llm.chat(
            messages=[
                {
                    "role": "system",
                    "content": PLANNER_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ]
        )

        content = (
            response.choices[0]
            .message
            .content
        )

        # Convert LLM JSON → Python dictionary
        data = json.loads(content)

        # Convert dictionary → PlanStep objects
        steps = [
            PlanStep(
                action=step["action"],
                arguments=step.get(
                    "arguments",
                    {},
                ),
            )
            for step in data["steps"]
        ]

        # Convert everything → Plan object
        plan = Plan(
            goal=data["goal"],
            steps=steps,
        )

        # Validate the LLM-generated plan
        validate_plan(plan)

        return plan