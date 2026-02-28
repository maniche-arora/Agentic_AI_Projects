# Analyser GPT — Architecture

This document explains the high-level architecture of the Analyser GPT project and includes a Mermaid diagram that shows component interactions.

## Diagram

```mermaid
flowchart LR
  subgraph User
    A[Browser / User] -->|upload file + ask task| Streamlit[Streamlit app
(streamlit_app.py)]
  end

  subgraph HostFS
    TempDir[(WORK_DIR_DOCKER: temp/)]
  end

  Streamlit -->|saves file to| TempDir
  Streamlit -->|calls| Main[main.py]
  Streamlit -->|starts| Team[DataAnalyzerTeam]

  subgraph Agents
    DataAgent[Data_Analyzer_Agent]
    CodeAgent[Code_Executor_Agent]
    Team --> DataAgent
    Team --> CodeAgent
  end

  DataAgent -->|uses| ModelClient[get_model_client()
(OpenAI client)]
  ModelClient -->|calls OpenAI API| OpenAI[OpenAI API]

  CodeAgent -->|executes code in| Docker[Docker container
(analyzer-gpt:latest)]
  Docker -->|mounts| TempDir
  Docker -->|reads/writes files| TempDir
  CodeAgent -->|sends results| Team
  Team -->|streams messages/results| Streamlit

  subgraph RepoFiles
    Req[requirements.txt]
    Dockerfile[Dockerfile
(custom image: pandas,numpy,matplotlib,seaborn,...)]
    Const[config/constants.py]
    DockerUtils[config/docker_utils.py]
    Prompts[agents/prompts/*]
  end

  Dockerfile -->|builds| Docker
  Req -->|dev deps used by host| Streamlit
  Const -->|WORK_DIR_DOCKER| TempDir
  DockerUtils -->|creates Docker executor| CodeAgent
  Prompts -->|system messages| DataAgent

  style TempDir fill:#fff7e6,stroke:#f39c12
  style Docker fill:#e8f6ff,stroke:#0b66ff
  style Streamlit fill:#e6fff1,stroke:#0bbf6b
  style DataAgent fill:#fff0f6,stroke:#ff4d6d
  style CodeAgent fill:#fff0f6,stroke:#ff4d6d
  style ModelClient fill:#f0f0f0,stroke:#666
  style OpenAI fill:#f7f7fb,stroke:#9b59b6
  classDef smallFont font-size:12px;
  class TempDir,Docker,Streamlit smallFont;
```

## Explanation (short)

- `streamlit_app.py` is the user-facing UI: users upload a file and enter a task. Uploaded files are saved to `WORK_DIR_DOCKER` (host `temp/`).
- `main.py` contains a CLI entrypoint with the same agent/team workflow used by Streamlit.
- `Data_Analyzer_Agent` constructs analysis code and prompts the `Code_Executor_Agent` to run it.
- `Code_Executor_Agent` runs code inside a Docker container built from `Dockerfile` (image `analyzer-gpt:latest`). The container uses the host `temp/` directory as its workspace so it can read uploaded files and write outputs (e.g. PNGs).
- `config/constants.py` defines `WORK_DIR_DOCKER` and `DOCKER_IMAGE`; `config/docker_utils.py` creates the `DockerCommandLineCodeExecutor` that launches the container.
- `agents/prompts/*` contains system prompts that guide agent behavior.

## How to export the diagram as PNG or SVG

If you want an image file of the diagram locally, you can use one of these options:

- Use a Mermaid rendering VS Code extension to open `docs/architecture.md` and export PNG/SVG.
- Use the `mmdc` (Mermaid CLI) tool:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/architecture.md -o docs/architecture.png
```

- Or open the diagram in an online Mermaid live editor and export.

---

If you want, I can also add an exported PNG/SVG to the repo (e.g., `docs/architecture.png`) and update the repository `README.md` to include the diagram and short explanation. Do you want me to add the exported image file now?