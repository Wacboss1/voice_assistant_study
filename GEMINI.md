# GEMINI.md

This project is a Python-based voice AI assistant built using the LiveKit Agents framework. It serves as a starter kit for creating voice AI applications.

## Project Overview

The core of the project is a voice AI assistant that uses a pipeline of models for speech-to-text (AssemblyAI), language modeling (OpenAI), and text-to-speech (Cartesia). The project is structured to be easily extensible.

- **Main Technologies:** Python, LiveKit Agents, OpenAI, Cartesia, AssemblyAI
- **Architecture:** The main application logic is in `src/agent.py`. The `Assistant` class defines the agent's behavior, and the `entrypoint` function sets up the voice AI pipeline.

## Building and Running

### Setup

1.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```
2.  Set up the environment by copying `.env.example` to `.env.local` and filling in the required keys:
    - `LIVEKIT_URL`
    - `LIVEKIT_API_KEY`
    - `LIVEKIT_API_SECRET`

### Running the Agent

-   **Download necessary models:**
    ```bash
    uv run python src/agent.py download-files
    ```
-   **Run in console mode:**
    ```bash
    uv run python src/agent.py console
    ```
-   **Run in development mode (for use with a frontend):**
    ```bash
    uv run python src/agent.py dev
    ```
-   **Run in production mode:**
    ```bashsx
    uv run python src/agent.py start
    ```

### Testing

-   Run tests with `pytest`:
    ```bash
    uv run pytest
    ```

## Development Conventions

-   **Linting and Formatting:** The project uses `ruff` for code linting and formatting.
    -   `uv run ruff format`
    -   `uv run ruff check`
-   **Coding Agents:** The `AGENTS.md` file indicates that this project is designed to be used with coding agents like Gemini. For more detailed instructions on developing within the `livekit-agent-starter-python` project, please refer to the `LiveKit/agent-starter-python/AGENTS.md` file.
-   **Extensibility:** New tools can be added to the agent using the `@function_tool` decorator.
-   **Test-Driven Development:** When modifying core agent behavior, it is recommended to use test-driven development.
-   **LiveKit CLI:** The `lk` CLI can be used for various tasks, with user approval.