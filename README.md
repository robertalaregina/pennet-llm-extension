# PEnnet LLM Extension

## Overview

This repository contains a Python-based experimental extension to the PEnnet threat modeling workflow. It uses a locally executed Large Language Model (LLM) to generate pre-conditions and post-conditions for threats in an existing threat catalogue.

The generated conditions are compared with the reference values in the catalogue to measure agreement.

## Objectives

- Generate pre-conditions and post-conditions for existing threats.
- Integrate a local LLM through Ollama.
- Compare generated conditions with reference values.
- Export structured results for analysis.

## Technologies

- Python
- Ollama
- Llama 3 (`llama3:latest`)
- pandas
- requests
- openpyxl

## Model Configuration

The script uses the model identifier `llama3:latest` through Ollama's local HTTP API:

`http://localhost:11434/api/generate`

The model runs locally. The exact Ollama version, model quantization, and any additional generation parameters should be recorded from the experimental environment.

## Repository Structure

```text
pennet-llm-extension/
├── data/
│   └── README.md
├── results/
│   └── README.md
├── generate_conditions.py
├── requirements.txt
└── README.md
```

## Input Data

Place the input Excel workbook at:

`data/threat_catalogue.xlsx`

The workbook must contain the columns expected by the script, including threat identifiers, asset information, threat descriptions, STRIDE categories, and reference pre-conditions and post-conditions.

## Output

The script writes the results to:

`results/llama_conditions_results.xlsx`

The output includes the reference and generated conditions, matching scores, and the raw model response when available.

## Workflow

1. Load the threat catalogue from Excel.
2. Extract each threat's information.
3. Construct a prompt containing the threat details.
4. Send the prompt to Ollama.
5. Parse and validate the JSON response.
6. Compare the generated conditions with the reference values.
7. Export the results to Excel.

## Condition Representation

The model returns three values in the order Confidentiality (C), Integrity (I), and Availability (A), for both pre-conditions and post-conditions.

- `n`: no impact
- `p`: partial impact
- `f`: full impact

The expected response contains `PreCondition` and `PostCondition` arrays, each with exactly three values.

## Installation

Install Python 3 and Ollama. Download the model:

```bash
ollama pull llama3:latest
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Ensure that Ollama is running before executing the script.

## Execution

From the repository root, run:

```bash
python generate_conditions.py
```

The script expects the input file at `data/threat_catalogue.xlsx` and creates the output directory and result file automatically.

## Evaluation

Each generated pre-condition and post-condition is compared with the corresponding reference values. The script reports matches for the pre-condition (out of 3), post-condition (out of 3), and combined score (out of 6).

Agreement with the reference catalogue is a measure of correspondence; it does not independently guarantee semantic correctness.

## Security and Privacy

- Do not commit passwords, API keys, access tokens, or personal credentials.
- Review input and output files before sharing them.
- Do not publish confidential or personal information.
- Local inference does not automatically guarantee that the host system and files are secure.

## Limitations

- Output quality depends on the threat descriptions and the model's response.
- The model may generate invalid or incorrect values.
- Results should be reviewed against the reference catalogue.
- Results may vary with model versions and configurations.

## Reproducibility

For reproducibility, record the Python version, Ollama version, exact model version, prompt, generation settings, and input dataset structure used in the experiment.

## License

Before distributing this code publicly, verify the licensing conditions of the original PEnnet project and all third-party components. No license has been specified for this repository yet.
