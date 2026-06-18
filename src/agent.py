import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.prompts import SYSTEM_PROMPT
from src.tools import calculator, convert_currency, add_tax


def build_prompt(user_request: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Demande utilisateur :
{user_request}
"""


def run_agent(user_request: str) -> str:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY est introuvable. Vérifie ton fichier .env."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=build_prompt(user_request),
        config=types.GenerateContentConfig(
            tools=[
                calculator,
                convert_currency,
                add_tax,
            ],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                maximum_remote_calls=5
            ),
        ),
    )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent Gemini avec tools : calculatrice, conversion, TVA."
    )

    parser.add_argument(
        "--ask",
        type=str,
        required=True,
        help="Demande utilisateur en langage naturel.",
    )

    args = parser.parse_args()

    try:
        answer = run_agent(args.ask)
        print("\n--- Réponse agent ---")
        print(answer)

    except EnvironmentError as error:
        print(f"Erreur environnement : {error}")

    except Exception as error:
        print(f"Erreur inattendue : {error}")


if __name__ == "__main__":
    main()