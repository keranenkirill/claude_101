# Claude 101 Learning Repository

A small learning repository for studying the **Claude Platform** through practical Python demos.

This repository works as my personal **sandbox environment**. I can modify the code, run different versions, break things and test ideas to see how Claude tools and technologies behave in practice.

The goal is to turn theory into code and understand the **differences, benefits and use cases** of the technologies covered in **Claude Platform 101**.

---

## Topics covered so far

### 1. Claude Platform Basics

Introduction to the Claude Platform and the main building blocks used in Claude applications.

### 2. Anthropic SDK & Messages API

Using Python to send requests to Claude and process model responses.

### 3. Messages, Content Blocks & Thinking

Understanding response blocks, token usage, stop reasons and Claude's thinking modes.

### 4. Tool Use

Giving Claude access to custom Python tools and understanding `tool_use` and `tool_result`.

### 5. Agent Loops

Building multi-step workflows where Claude can call tools, receive results and continue until the task is complete.

### 6. Built-in Tools

Testing Claude's server-side tools:

- Web Search
- Web Fetch
- Code Execution

### 7. Claude Skills

Creating and using reusable custom Skills together with Claude and built-in tools.

### 8. Model Context Protocol (MCP)

Connecting Claude to external services through MCP servers.

Current experiment: **Notion MCP**.

---

## Technologies used

- Python
- Anthropic Python SDK
- Claude Messages API
- Extended / Adaptive Thinking
- Tool Use
- JSON Schema
- Agent Loops
- Tool Runner
- Web Search
- Web Fetch
- Code Execution
- Claude Skills
- Model Context Protocol (MCP)
- OAuth
- Notion MCP
- python-dotenv
- pathlib
- Git & GitHub
- VS Code
- Python virtual environments

---

## Mini demos

### `test_models.py`

Compares different Claude models using the same prompt.

The demo measures response time and token usage to make model differences easier to observe in practice.

### `packing_thinking.py`

A small demo for Claude's **extended thinking**.

It shows the summarized thinking block, the final answer and token usage for a simple travel-planning task.

### `built_in_tools.py`

Demonstrates Claude's server-side **Web Search, Web Fetch and Code Execution** tools.

The script also prints the different response block types returned by these tools.

### `weather_agent_loop.py`

A fully manual tool-use and agent-loop example.

Claude can choose between `get_weather` and `get_forecast`, while the Python program manually handles tool calls, tool results, conversation history and loop control.

### `weather_tool_runner.py`

Implements the same weather-agent idea using Anthropic's **Tool Runner**.

This makes it easy to compare a manually written agent loop with the SDK's higher-level automated tool-running approach.

### `miniweather_toolrun.py`

A minimal Tool Runner example with a single `get_weather` tool.

Its purpose is to show the smallest practical version of automatic Claude tool execution.

### `python_release_skill.py`

Demonstrates a custom **Claude Skill** together with Web Search, Web Fetch, Code Execution and adaptive thinking.

The demo uploads or reuses a Skill and uses it to produce a structured Python release brief.

### `notion_mcp_demo.py`

Connects Claude to a **Notion MCP server**.

The demo lets Claude search a Notion workspace through server-side MCP tools while keeping the test read-only.
