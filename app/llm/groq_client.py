from groq import Groq


class GroqClient:

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self.client = Groq(
            api_key=api_key
        )

        self.model = model

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ):
        
        print(
    "TOOLS SENT:",
    [
        tool["function"]["name"]
        for tool in (tools or [])
    ],
)

        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        return self.client.chat.completions.create(
            **kwargs
        )