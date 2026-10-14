# PEnnet LLM Extension

## Overview

This repository contains the Python implementation of an experimental extension to the PEnnet threat modeling workflow. The extension integrates a locally executed Large Language Model (LLM) to generate pre-conditions and post-conditions for threats already included in the PEnnet Threat Catalogue.

The generated conditions are compared with the corresponding reference values to evaluate the model's output.

## Objectives

- Automate the generation of pre-conditions and post-conditions associated with existing threats.
- Integrate a local LLM into the threat modeling workflow.
- Compare generated conditions with the reference Threat Catalogue.
- Export structured results for subsequent analysis.

## Workflow

1. Read the threat catalogue from an Excel file.
2. Extract the information describing each threat.
3. Construct a prompt containing the threat details.
4. Send the prompt to the LLM through Ollama.
5. Parse the model response in JSON format.
6. Compare generated conditions with the reference values.
7. Export the results to an Excel file.

## Technology Stack

- **Programming language:** Python
- **LLM runtime:** Ollama
- **Model:** Llama 3
- **Input format:** Excel (`.xlsx`)
- **Output format:** Excel (`.xlsx`)
- **LLM response format:** JSON

## Model Configuration

The implementation uses the Ollama model identifier `llama3:latest` and communicates with the local endpoint:

`http://localhost:11434/api/generate`

The model is executed locally. The exact model version, quantization, and generation parameters should be documented according to the configuration used in the experiment.

## Pre-conditions and Post-conditions

For each threat, the model evaluates the impact on:

- **Confidentiality (C)**
- **Integrity (I)**
- **Availability (A)**

The expected values are:

- `n`: no impact
- `p`: partial impact
- `f`: full impact

The expected JSON response contains two arrays:

- `PreCondition`: values representing the conditions before the threat occurs.
- `PostCondition`: values representing the conditions after the threat occurs.

Example of the expected output structure:

```json
{
  "PreCondition": ["n", "n", "n"],
  "PostCondition": ["n", "n", "f"]
}
```

The values above are illustrative and do not represent the assessment of a specific threat.

## Evaluation

The generated values are compared with the corresponding values in the original catalogue. The output includes the threat identifier, reference conditions, generated conditions, matching scores, and the raw model response when available.

The comparison measures agreement with the reference catalogue; it does not independently guarantee the semantic correctness of the generated conditions.

## Requirements

- Python 3
- Ollama
- Llama 3 available through Ollama
- Python packages listed in `requirements.txt`
- An input Excel file containing the columns expected by the script

## Installation

Install Ollama and download the model:

```bash
ollama pull llama3:latest
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Verify that the model is available:

```bash
ollama list
```

Ensure that Ollama is running before executing the Python script.

## Execution

Run the Python script from the project directory:

```bash
python src/generate_conditions.py
```

The input and output paths must be configured according to the instructions provided with the implementation.

## Security and Privacy

- No API keys, passwords, or personal credentials are required for the local Ollama endpoint used by this implementation.
- Input datasets and generated results should be checked for confidential or personal information before publication.
- Local execution does not by itself guarantee the security of the host machine or its files.
- Generated conditions should be reviewed before being used in security assessments.

## Limitations

- Results depend on the quality and completeness of the threat descriptions.
- The model may produce malformed JSON or incorrect assessments.
- Generated values should be validated against the reference catalogue.
- Results may vary with the model version and generation configuration.

## Reproducibility

For reproducibility, document the Python and Ollama versions, exact model identifier, prompt, generation parameters, input dataset structure, and package versions used in the experiment.

## License

The repository license has not yet been specified. Before distributing the code publicly, verify the licensing conditions of the original PEnnet project and any third-party components.
