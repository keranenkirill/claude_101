"""
notion_mcp_demo.py

Claude Platform 101 - luku 9: MCP-demo Notionilla.

Tässä käytetään Anthropicin SERVER-SIDE MCP CONNECTORIA:
- mcp_servers kertoo MISSÄ Notion MCP on ja miten siihen autentikoidutaan
- mcp_toolset kertoo MITÄ MCP-serverin työkaluja Claude saa käyttää

Python ei määrittele Notion-työkalujen schemaa eikä suorita niitä itse.
Notion MCP julkaisee työkalut, ja Claude API kutsuu niitä MCP:n kautta.
"""

import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


# ============================================================
# 1. ASETUKSET
# ============================================================

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env.local")

client = Anthropic()

MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5")

NOTION_MCP_URL = "https://mcp.notion.com/mcp"
NOTION_MCP_TOKEN = os.getenv("NOTION_MCP_TOKEN")

if not NOTION_MCP_TOKEN:
    raise RuntimeError(
        "NOTION_MCP_TOKEN puuttuu .env.local-tiedostosta. "
        "Aja ensin notion_mcp_login.py."
    )


# ============================================================
# 2. DEMON PYYNTÖ
# ============================================================

# Ensimmäinen testi on tarkoituksella READ-ONLY-tyyppinen:
# pyydämme Claudea etsimään Notionista sisältöä, mutta emme luomaan,
# muuttamaan tai poistamaan mitään.
USER_REQUEST = (
    "Use the connected Notion tools. "
    "Search my Notion workspace for pages related to work and school "
    "For each result, give the page title and a one-sentence explanation. "
    "Do not create, edit, move, archive, or delete anything."
)


# ============================================================
# 3. VASTAUKSEN TULOSTUS
# ============================================================

def print_response(response) -> None:
    """Tulosta MCP-kutsut, MCP-tulokset ja Clauden lopullinen teksti."""

    print("\n" + "=" * 70)
    print("NOTION MCP DEMO")
    print("=" * 70)

    print(f"stop_reason: {response.stop_reason}")

    for block in response.content:
        print(f"\n[{block.type}]")

        if block.type == "mcp_tool_use":
            print(f"Serveri: {block.server_name}")
            print(f"Työkalu: {block.name}")
            print(f"Syöte: {block.input}")

        elif block.type == "mcp_tool_result":
            print(f"Tool use ID: {block.tool_use_id}")
            print(f"Virhe: {block.is_error}")

            # Tuloksen sisältö voi sisältää eri MCP-content-tyyppejä,
            # joten tulostetaan se oppimisdemoa varten sellaisenaan.
            print(f"Tulos: {block.content}")

        elif block.type == "text":
            print(block.text)

        else:
            print(block)


# ============================================================
# 4. MCP-KUTSU
# ============================================================

response = client.beta.messages.create(
    model=MODEL,
    max_tokens=3000,

    # Luvun 9 ydinosa 1:
    # MCP-serverin yhteystiedot + OAuth bearer token.
    mcp_servers=[
        {
            "type": "url",
            "url": NOTION_MCP_URL,
            "name": "notion",
            "authorization_token": NOTION_MCP_TOKEN,
        }
    ],

    # Luvun 9 ydinosa 2:
    # Otetaan Notion MCP:n työkalut Clauden käyttöön.
    #
    # Ensimmäisessä demossa annamme kaikki työkalut näkyviin,
    # MUTTA system/user prompt käskee tekemään vain hakua.
    #
    # Seuraavassa harjoituksessa tämä kannattaa vaihtaa
    # varsinaiseksi allowlistiksi, kun näemme palvelimen oikeat
    # työkalunimet ensimmäisen ajon tulosteesta.
    tools=[
        {
            "type": "mcp_toolset",
            "mcp_server_name": "notion",
        }
    ],

    # MCP connector on edelleen beta-ominaisuus.
    betas=["mcp-client-2025-11-20"],

    system=(
        "You are a careful Notion research assistant. "
        "This is a learning demo. "
        "Only read/search content unless the user explicitly asks "
        "for a write operation. "
        "Never delete or archive content."
    ),

    messages=[
        {
            "role": "user",
            "content": USER_REQUEST,
        }
    ],
)


# ============================================================
# 5. TULOSTUS
# ============================================================

print_response(response)
