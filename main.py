import os

from dotenv import load_dotenv

from app.agent.runner import Agent
from app.llm.groq_client import GroqClient


load_dotenv()


def main():

    llm = GroqClient(
        api_key=os.environ["GROQ_API_KEY"],
        model=os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b",
        ),
    )

    agent = Agent(
        llm=llm,
        max_iterations=5,
    )

    print("🧠 MILO")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You > ")

        if user_input.lower() in {
            "exit",
            "quit",
        }:
            break

        if not user_input.strip():
            continue

        try:

            response = agent.run(
                user_input
            )

            print(
                f"\nMILO > {response}\n"
            )

        except Exception as exc:

            print(
                f"\n❌ Error: {exc}\n"
            )


if __name__ == "__main__":
    main()