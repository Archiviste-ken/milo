import os

from dotenv import load_dotenv

from app.llm.groq_client import GroqClient


load_dotenv()


def main():

    agent = GroqClient(
        api_key=os.environ["GROQ_API_KEY"],
        model="openai/gpt-oss-120b",
    )

    print("🧠 MILO")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You > ")

        if user_input.lower() in {"exit", "quit"}:
            break

        response = agent.chat(user_input)

        print(f"\nMILO > {response}\n")


if __name__ == "__main__":
    main()