from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv(".env.local")

client = Anthropic()


response = client.messages.create(
    model="claude-haiku-4-5",

    # Sisältää sekä thinking-vaiheen että lopullisen vastauksen.
    max_tokens=4096,

    # Haiku 4.5 käyttää manuaalista extended thinking -tilaa.
    thinking={
        "type": "enabled",
        "budget_tokens": 2048,
        "display": "summarized",
    },

    messages=[
        {
            "role": "user",
            "content": (
                "I'm packing for a three-day trip to Denver. "
                "The temperature is -2°C today, 0°C tomorrow, "
                "4°C on day two and 7°C on day three. "
                "Create a practical packing plan and explain "
                "the trade-offs."
            ),
        }
    ],
)


print(f"Stop reason: {response.stop_reason}")


for block in response.content:

    if block.type == "thinking":
        print("\n--- AJATTELUN YHTEENVETO ---")
        print(block.thinking)

    elif block.type == "text":
        print("\n--- LOPULLINEN VASTAUS ---")
        print(block.text)


print("\n--- TOKENIEN KÄYTTÖ ---")
print(response.usage)
