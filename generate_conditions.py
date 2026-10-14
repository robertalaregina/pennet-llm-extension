import json
from pathlib import Path

import pandas as pd
import requests

# Paths are relative to the repository root.
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_EXCEL = BASE_DIR / "data" / "threat_catalogue.xlsx"
OUTPUT_EXCEL = BASE_DIR / "results" / "llama_conditions_results.xlsx"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:latest"
REQUEST_TIMEOUT = 300

REQUIRED_COLUMNS = [
    "Threat ID", "Asset", "Asset Type", "Threat", "STRIDE",
    "Threat Description", "PreC", "PreI", "PreA", "PostC", "PostI", "PostA",
]


def ask_llama(row):
    """Generate pre-conditions and post-conditions for one threat."""
    prompt = f"""You are a threat modeling expert.

Analyze this threat:

Threat ID: {row['Threat ID']}
Asset: {row['Asset']}
Asset Type: {row['Asset Type']}
Threat: {row['Threat']}
STRIDE: {row['STRIDE']}
Description: {row['Threat Description']}

Determine the impact on:
C = Confidentiality
I = Integrity
A = Availability

Use ONLY these values:
"n" = no impact
"p" = partial impact
"f" = full impact

IMPORTANT:
- PreCondition MUST contain exactly 3 values: C, I, A
- PostCondition MUST contain exactly 3 values: C, I, A
- Do NOT write explanations.
- Do NOT write Markdown.
- Return ONLY ONE valid JSON object.

Example:
{{"PreCondition":["n","n","p"],"PostCondition":["f","p","f"]}}

Return ONLY the JSON object."""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    raw_text = response.json()["response"].strip()
    data = json.loads(raw_text)

    pre = data["PreCondition"]
    post = data["PostCondition"]

    if not isinstance(pre, list) or len(pre) != 3:
        raise ValueError("PreCondition must contain exactly 3 values")
    if not isinstance(post, list) or len(post) != 3:
        raise ValueError("PostCondition must contain exactly 3 values")
    if any(value not in ["n", "p", "f"] for value in pre + post):
        raise ValueError("Invalid condition value; expected n, p, or f")

    return ",".join(pre), ",".join(post), raw_text


def normalize_reference_values(row, columns):
    """Normalize reference catalogue values for comparison."""
    return ",".join(str(row[column]).strip().lower() for column in columns)


def main():
    if not INPUT_EXCEL.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_EXCEL}\n"
            "Place the Excel threat catalogue at data/threat_catalogue.xlsx."
        )

    df = pd.read_excel(INPUT_EXCEL)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(
            "The input Excel file is missing required columns: "
            + ", ".join(missing_columns)
        )

    OUTPUT_EXCEL.parent.mkdir(parents=True, exist_ok=True)
    results = []

    for index, row in df.iterrows():
        print(f"[{index + 1}/{len(df)}] {row['Threat ID']} - {row['Threat']}")
        try:
            pre, post, raw = ask_llama(row)
            catalog_pre = normalize_reference_values(row, ["PreC", "PreI", "PreA"])
            catalog_post = normalize_reference_values(row, ["PostC", "PostI", "PostA"])

            pre_match = sum(
                expected == generated
                for expected, generated in zip(catalog_pre.split(","), pre.split(","))
            )
            post_match = sum(
                expected == generated
                for expected, generated in zip(catalog_post.split(","), post.split(","))
            )

            results.append({
                "Threat ID": row["Threat ID"],
                "Threat": row["Threat"],
                "Catalog PreCondition": catalog_pre,
                "Llama PreCondition": pre,
                "Pre Match": f"{pre_match}/3",
                "Catalog PostCondition": catalog_post,
                "Llama PostCondition": post,
                "Post Match": f"{post_match}/3",
                "Total Match": f"{pre_match + post_match}/6",
                "Llama Raw Response": raw,
            })
        except Exception as error:
            results.append({
                "Threat ID": row["Threat ID"],
                "Threat": row["Threat"],
                "Error": str(error),
            })

    pd.DataFrame(results).to_excel(OUTPUT_EXCEL, index=False)
    print("\nFinished.")
    print(f"Results saved to: {OUTPUT_EXCEL}")


if __name__ == "__main__":
    main()
