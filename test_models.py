from time import perf_counter

from anthropic import Anthropic
from dotenv import load_dotenv


# Lataa API-avain .env.local-tiedostosta
load_dotenv(".env.local")

# SDK lukee ANTHROPIC_API_KEY-muuttujan automaattisesti
client = Anthropic()

prompt = (
    "Explain what an API is to a beginner in exactly two sentences."
)

models = [
    "claude-haiku-4-5",
    "claude-sonnet-5",
    "claude-opus-5",
]

for model in models:
    start_time = perf_counter()

    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    elapsed_time = perf_counter() - start_time

    print(f"\n=== {model} ===")

    for block in response.content:
        if block.type == "text":
            print(block.text)

    print(f"Vastausaika: {elapsed_time:.2f} sekuntia")
    print(f"Syötetokenit: {response.usage.input_tokens}")
    print(f"Vastaustokenit: {response.usage.output_tokens}")