import json

from anthropic import Anthropic
from dotenv import load_dotenv


# ============================================================
# 1. ASETUKSET
# ============================================================

load_dotenv(".env.local")

client = Anthropic()

MODEL = "claude-haiku-4-5"
MAX_TURNS = 10

USER_REQUEST = (
    "I'm packing for a three-day trip to Denver. "
    "What is the weather today and over the next few days? "
    "Give me packing advice after checking the available tools."
)


# ============================================================
# 2. VARSINAISET PYTHON-FUNKTIOT
# ============================================================

def get_weather(city: str) -> str:
    """
    Palauttaa tämänhetkisen sään.

    Tässä harjoituksessa data on kovakoodattu.
    Oikeassa sovelluksessa tässä kutsuttaisiin sää-API:a.
    """

    weather_data = {
        "city": city,
        "temperature_celsius": -2,
        "condition": "light snow",
        "wind": "moderate",
    }

    return json.dumps(weather_data, ensure_ascii=False)


def get_forecast(city: str) -> str:
    """
    Palauttaa tulevien kolmen päivän sääennusteen.

    Tässä harjoituksessa data on kovakoodattu.
    """

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

    return json.dumps(forecast_data, ensure_ascii=False)


# ============================================================
# 3. CLAUDELLE NÄYTETTÄVÄT TYÖKALUKUVAUKSET
# ============================================================

TOOLS = [
    {
        "name": "get_weather",
        "description": (
            "Get the current weather conditions for a city. "
            "Use this tool for today's weather only. "
            "It does not provide future forecasts."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": (
                        "The city whose current weather should be checked"
                    ),
                }
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_forecast",
        "description": (
            "Get the weather forecast for the next three days for a city. "
            "Use this tool for future weather, not current conditions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": (
                        "The city whose three-day forecast should be checked"
                    ),
                }
            },
            "required": ["city"],
        },
    },
]


# ============================================================
# 4. TYÖKALUREITITIN
# ============================================================

TOOL_HANDLERS = {
    "get_weather": get_weather,
    "get_forecast": get_forecast,
}


def run_tool(name: str, tool_input: dict) -> str:
    """
    Valitsee oikean Python-funktion Clauden ilmoittaman
    työkalun nimen perusteella.
    """

    function = TOOL_HANDLERS.get(name)

    if function is None:
        raise ValueError(f"Unknown tool: {name}")

    print(f"Python löysi funktion: {function.__name__}")
    print(f"Python suorittaa syötteellä: {tool_input}")

    # Esimerkiksi:
    # {"city": "Denver"}
    #
    # muuttuu muotoon:
    # get_weather(city="Denver")
    result = function(**tool_input)

    return result


# ============================================================
# 5. KESKUSTELUHISTORIA
# ============================================================

messages = [
    {
        "role": "user",
        "content": USER_REQUEST,
    }
]


# ============================================================
# 6. MANUAALINEN AGENTTISILMUKKA
# ============================================================

for turn_number in range(1, MAX_TURNS + 1):

    print("\n" + "=" * 70)
    print(f"AGENTTIKIERROS {turn_number}")
    print("=" * 70)

    print(f"Messages-listassa on {len(messages)} viestiä.")

    # Lähetetään työkalukuvaukset ja keskusteluhistoria Claudelle.
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=(
            "You are a travel assistant. "
            "Use the available weather tools whenever current or "
            "future weather information is required. "
            "Do not invent weather information."
        ),
        tools=TOOLS,
        messages=messages,
    )

    print(f"Claude palautti stop_reason-arvon: {response.stop_reason}")

    # Kerätään erikseen tekstilohkot ja työkalupyynnöt.
    text_blocks = []
    tool_use_blocks = []

    for block in response.content:

        print(f"Vastauksessa oleva lohkotyyppi: {block.type}")

        if block.type == "text":
            text_blocks.append(block.text)

        elif block.type == "tool_use":
            tool_use_blocks.append(block)

    # Claude voi kirjoittaa tekstiä myös ennen työkalupyyntöä.
    if text_blocks:
        print("\nClauden tämän kierroksen teksti:")

        for text in text_blocks:
            print(text)

    # ========================================================
    # 7. CLAUDE ON VALMIS
    # ========================================================

    if response.stop_reason == "end_turn":

        print("\n--- LOPULLINEN VASTAUS ---")

        if text_blocks:
            for text in text_blocks:
                print(text)
        else:
            print("Claude ei palauttanut tekstisisältöä.")

        print("\nAgenttisilmukka päättyy.")
        break

    # ========================================================
    # 8. CLAUDE PYYTÄÄ TYÖKALUJA
    # ========================================================

    if response.stop_reason == "tool_use":

        print(
            f"\nClaude pyysi tällä kierroksella "
            f"{len(tool_use_blocks)} työkalua."
        )

        # Clauden koko vastaus tallennetaan historiaan.
        messages.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        tool_results = []

        for tool_call in tool_use_blocks:

            print("\n--- TYÖKALUPYYNTÖ ---")
            print(f"ID: {tool_call.id}")
            print(f"Nimi: {tool_call.name}")
            print(f"Syöte: {tool_call.input}")

            result = run_tool(
                name=tool_call.name,
                tool_input=tool_call.input,
            )

            print(f"Työkalun tulos: {result}")

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": result,
                }
            )

        # Kaikki tämän kierroksen työkalutulokset lähetetään
        # yhdessä user-viestissä.
        messages.append(
            {
                "role": "user",
                "content": tool_results,
            }
        )

        print(
            f"\nTyökalutulokset lisättiin historiaan. "
            f"Messages-listassa on nyt {len(messages)} viestiä."
        )

        # for-silmukka aloittaa seuraavan agenttikierroksen.
        continue

    # ========================================================
    # 9. MUU PYSÄYTYSSYY
    # ========================================================

    raise RuntimeError(
        f"Unexpected stop reason: {response.stop_reason}"
    )

else:
    raise RuntimeError(
        f"Agent did not finish within {MAX_TURNS} turns"
    )