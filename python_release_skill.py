import os
from pathlib import Path

from anthropic import Anthropic
from anthropic.lib import files_from_dir
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
SKILL_DIR = BASE_DIR / "skills" / "python-release-brief"

load_dotenv(BASE_DIR / ".env.local")

client = Anthropic()
model = os.getenv("CLAUDE_MODEL", "claude-opus-5")


def get_skill_id() -> str:
    """Palauta olemassa oleva ID tai lataa Skill kerran."""

    skill_id = os.getenv("DEMO_SKILL_ID")

    if skill_id:
        print(f"Käytetään tallennettua Skilliä: {skill_id}")
        return skill_id

    skill = client.skills.create(
        display_name="Python Release Brief",
        files=files_from_dir(str(SKILL_DIR)),
    )

    print(f"Uusi Skill ladattiin: {skill.id}")
    print("Lisää tämä .env.local-tiedostoon:")
    print(f"DEMO_SKILL_ID={skill.id}\n")

    return skill.id


skill_id = get_skill_id()

request = (
    "Selvitä python.org-sivustolta kolme viimeisintä vakaata Python 3:n "
    "vuosittaista feature release -versiota. Älä laske patch-julkaisuja. "
    "Käytä web searchia julkaisusivujen löytämiseen ja web fetchiä niiden "
    "lukemiseen. Laske code executionilla päivien määrä peräkkäisten "
    "GA-julkaisupäivien välillä. Tee lopuksi Skillin mukainen suomenkielinen "
    "briiffi ja merkitse lähteet."
)

response = client.messages.create(
    model=model,
    max_tokens=8000,
    system=(
        "Olet huolellinen teknologiatutkija. "
        "Älä keksi puuttuvia tietoja."
    ),
    thinking={"type": "adaptive", "display": "summarized"},
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": skill_id,
                "version": "latest",
            }
        ]
    },
    tools=[
        {
            "type": "web_search_20260209",
            "name": "web_search",
            "max_uses": 4,
            "allowed_domains": ["python.org"],
        },
        {
            "type": "web_fetch_20260209",
            "name": "web_fetch",
            "max_uses": 4,
            "allowed_domains": ["python.org"],
            "citations": {"enabled": True},
            "max_content_tokens": 20000,
        },
        {
            "type": "code_execution_20260120",
            "name": "code_execution",
        },
    ],
    messages=[
        {
            "role": "user",
            "content": request,
        }
    ],
)

print(f"stop_reason: {response.stop_reason}")

for block in response.content:
    if block.type == "thinking" and block.thinking:
        print("\n--- AJATTELUN YHTEENVETO ---")
        print(block.thinking)

    elif block.type == "server_tool_use":
        print(f"\n[Server tool: {block.name}]")

    elif block.type == "text":
        print(block.text)
