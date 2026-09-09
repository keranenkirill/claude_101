from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(".env.local")

client = Anthropic()

buggy_code = """
function add(a, b) {
    return a - b;
}
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=2048,
    system=(
        "You are a terse senior code reviewer. "
        "Give feedback as one code line and short explanation."
    ),
    messages=[
        {
            "role": "user",
            "content": f"Review this code:\n{buggy_code}",
        }
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)