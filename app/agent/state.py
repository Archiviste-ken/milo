from dataclasses import dataclass, field


@dataclass
class AgentState:

    messages: list[dict] = field(
        default_factory=list
    )

    iteration: int = 0

    tool_calls: list[dict] = field(
        default_factory=list
    )

    observations: list[dict] = field(
        default_factory=list
    )

    verifications: list[dict] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    status: str = "idle"