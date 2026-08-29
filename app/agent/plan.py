from dataclasses import dataclass, field


@dataclass
class PlanStep:
    action: str
    arguments: dict = field(
        default_factory=dict
    )


@dataclass
class Plan:
    goal: str
    steps: list[PlanStep]