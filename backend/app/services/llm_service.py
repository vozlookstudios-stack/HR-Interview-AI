import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured in the .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={
        "api_version": "v1"
    }
)


MODEL_NAME = "gemini-3.6-flash"


def generate_content(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
        )

        if not interaction.output_text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return interaction.output_text.strip()

    except Exception as error:
        raise RuntimeError(
            f"Gemini API Error: {error}"
        ) from error