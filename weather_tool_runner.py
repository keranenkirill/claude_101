import json

from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv


# ============================================================
# 1. ASETUKSET
# ============================================================

load_dotenv(".env.local")

client = Anthropic()

MODEL = "claude-haiku-4-5"
MAX_ITERATIONS = 10

USER_REQUEST = (
    "I'm packing for a three-day trip to Denver. "
    "What is the weather today and over the next few days? "
    "Give me packing advice after checking the available tools."
)


# ============================================================
# 2. TYÖKALUT
# ============================================================

@beta_tool
def get_weather(city: str) -> str:
    """Get the current weather conditions for a city.

    Use this tool for today's current weather only.
    It does not provide future forecasts.

    Args:
        city: The city whose current weather should be checked
    """

    print("\n>>> PYTHON SUORITTAA get_weather-TYÖKALUN")
    print(f">>> Parametri city={city!r}")

    weather_data = {
        "city": city,
        "temperature_celsius": -2,
        "condition": "light snow",
        "wind": "moderate",
    }

    result = json.dumps(
        weather_data,
        ensure_ascii=False,
    )

    print(f">>> Työkalun palautusarvo: {result}")

    return result


@beta_tool
def get_forecast(city: str) -> str:
    """Get the weather forecast for the next three days for a city.

    Use this tool for future weather, not current conditions.

    Args:
        city: The city whose three-day forecast should be checked
    """

    print("\n>>> PYTHON SUORITTAA get_forecast-TYÖKALUN")
    print(f">>> Parametri city={city!r}")

    forecast_data = {
        "city": city,
        "forecast": [
            {
                "day": "tomorrow",
                "temperature_celsius": 0,
                "condition": "snow flurries",
            },
            {
                "day": "day 2",
                "temperature_celsius": 4,
                "condition": "partly cloudy",
            },
            {
                "day": "day 3",
                "temperature_celsius": 7,
                "condition": "sunny",
            },
        ],
    }

    result = json.dumps(
        forecast_data,
        ensure_ascii=False,
    )

    print(f">>> Työkalun palautusarvo: {result}")

    return result


# ============================================================
# 3. TOOL RUNNERIN LUOMINEN
# ============================================================

runner = client.beta.messages.tool_runner(
    model=MODEL,
    max_tokens=1024,
    max_iterations=MAX_ITERATIONS,
    system=(
        "You are a travel assistant. "
        "Use the available weather tools whenever current or "
        "future weather information is required. "
        "Do not invent weather information."
    ),
    tools=[
        get_weather,
        get_forecast,
    ],
    messages=[
        {
            "role": "user",
            "content": USER_REQUEST,
        }
    ],
)


# ============================================================
# 4. TOOL RUNNERIN KIERROSTEN SEURAAMINEN
# ============================================================

final_message = None

for turn_number, message in enumerate(runner, start=1):

    final_message = message

    print("\n" + "=" * 70)
    print(f"TOOL RUNNER -KIERROS {turn_number}")
    print("=" * 70)

    print(f"Stop reason: {message.stop_reason}")

    for block in message.content:

        print(f"\nLohkon tyyppi: {block.type}")

        if block.type == "tool_use":
            print("Claude pyytää työkalua.")
            print(f"Työkalun ID: {block.id}")
            print(f"Työkalun nimi: {block.name}")
            print(f"Työkalun syöte: {block.input}")

        elif block.type == "text":
            # Jos mukana on tool_use, tämä voi olla välitekstiä.
            if message.stop_reason == "tool_use":
                print("Clauden väliteksti:")
                print(block.text)


# ============================================================
# 5. LOPULLISEN VASTAUKSEN TULOSTAMINEN
# ============================================================

if final_message is None:
    raise RuntimeError("Tool Runner did not return any messages")


print("\n" + "=" * 70)
print("LOPULLINEN VASTAUS")
print("=" * 70)

final_text_found = False

for block in final_message.content:
    if block.type == "text":
        print(block.text)
        final_text_found = True

if not final_text_found:
    print("Claude ei palauttanut lopullista tekstisisältöä.")
