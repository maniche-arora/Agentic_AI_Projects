Analyser GPT — Architecture (Summary)

This short README explains the architecture of the Analyser GPT project and points to the full diagram in `docs/architecture.md`.

Key points:

- Streamlit provides the UI for uploading data and submitting tasks.
- The two-agent team consists of a `Data_Analyzer_Agent` and a `Code_Executor_Agent`.
- The Code Executor runs inside a Docker container using the custom image `analyzer-gpt:latest` which contains data-science libraries preinstalled.
- The host `temp/` directory (`WORK_DIR_DOCKER`) is shared with the container so uploaded files and generated outputs (images, CSVs) are accessible to both host and container.

See `docs/architecture.md` for a diagram and more details.
