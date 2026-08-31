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

    plan: list[str] = field(
        default_factory=list
    )

    current_step: int = 0
    retry_count: int = 0

    recovery_events: list[dict] = field(
    default_factory=list
)

    status: str = "idle"