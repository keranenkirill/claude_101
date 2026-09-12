from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv(".env.local")

client = Anthropic()

MODEL = "claude-opus-5"
DEMO = "all"  # search | fetch | code | all


def print_response(title: str, response) -> None:
    """Tulosta vastauksen tärkeät lohkot."""

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(f"stop_reason: {response.stop_reason}")

    for block in response.content:
        print(f"\n[{block.type}]")

        if block.type == "server_tool_use":
            print(f"Työkalu: {block.name}")
            print(f"Syöte: {block.input}")

        elif block.type == "web_search_tool_result":
            if isinstance(block.content, list):
                print(f"Hakutuloksia: {len(block.content)}")

                for result in block.content:
                    title = getattr(result, "title", None)
                    url = getattr(result, "url", None)

                    if title and url:
                        print(f"- {title}: {url}")
            else:
                print(block.content)

        elif block.type == "web_fetch_tool_result":
            result_type = getattr(block.content, "type", "unknown")
            url = getattr(block.content, "url", None)
            print(f"Tulos: {result_type}")

            if url:
                print(f"URL: {url}")

        elif block.type == "bash_code_execution_tool_result":
            print(f"stdout: {block.content.stdout}")

            if block.content.stderr:
                print(f"stderr: {block.content.stderr}")

            print(f"return_code: {block.content.return_code}")

        elif block.type == "text":
            print(block.text)

            for citation in getattr(block, "citations", []) or []:
                print(
                    f"Lähde: {citation.title} - {citation.url}"
                )

        else:
            print(block)


def run_web_search() -> None:
    """Hae ajankohtaista tietoa verkosta."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        tools=[
            {
                "type": "web_search_20260209",
                "name": "web_search",
                "max_uses": 3,
                "allowed_domains": [
                    "anthropic.com",
                    "claude.com",
                ],
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    "What is Anthropic's latest model release? "
                    "Use official sources and answer in one sentence."
                ),
            }
        ],
    )

    print_response("WEB SEARCH", response)


def run_web_fetch() -> None:
    """Lue käyttäjän antama verkkosivu."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        tools=[
            {
                "type": "web_fetch_20260209",
                "name": "web_fetch",
                "max_uses": 1,
                "allowed_domains": ["academy.claude.com"],
                "max_content_tokens": 8000,
                "citations": {"enabled": True},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    "Read this lesson and summarize its three main ideas: "
                    "https://academy.claude.com/courses/"
                    "claude-platform-101/built-in-tools"
                ),
            }
        ],
    )

    print_response("WEB FETCH", response)


def run_code_execution() -> None:
    """Laske tulos Anthropicin sandboxissa."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        tools=[
            {
                "type": "code_execution_20260120",
                "name": "code_execution",
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    "Use Python to calculate the mean and population "
                    "standard deviation of [1, 2, 3, 4, 5, 6, 7, "
                    "8, 9, 10]. Show the code and the result."
                ),
            }
        ],
    )

    print_response("CODE EXECUTION", response)


def main() -> None:
    """Aja valitut esimerkit."""

    if DEMO in {"search", "all"}:
        run_web_search()

    if DEMO in {"fetch", "all"}:
        run_web_fetch()

    if DEMO in {"code", "all"}:
        run_code_execution()


if __name__ == "__main__":
    main()
