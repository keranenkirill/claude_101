from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv
load_dotenv(".env.local")


client = Anthropic()


@beta_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: The city whose weather should be checked
    """
    return f"Weather in {city}: -2 °C and light snow"


runner = client.beta.messages.tool_runner(
    model="claude-haiku-4-5",
    max_tokens=1024,
    max_iterations=10,
    tools=[get_weather],
    messages=[
        {
            "role": "user",
            "content": "What should I wear in Denver today?",
        }
    ],
)

final_message = runner.until_done()
for b in final_message.content:
    print(b.text)
