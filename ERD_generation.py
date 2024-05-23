import os

from dbterd.api import DbtErd

GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR = os.getenv(
    "NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR"
)


def filter_lines(input_string):
    # Split the input string into lines
    lines = input_string.split("\n")

    # Initialize a flag to keep track of whether we are inside curly brackets
    inside_brackets = False

    # Filter out lines based on whether they are inside or outside curly brackets
    filtered_lines = []
    for line in lines:
        if "{" in line:
            inside_brackets = True
            filtered_lines.append(line)
        elif "}" in line:
            inside_brackets = False
            filtered_lines.append(line)
        elif not inside_brackets or "_sk" in line:
            filtered_lines.append(line)

    # Join the filtered lines back together
    result = "\n".join(filtered_lines)

    return result


erd = DbtErd(
    select=["wildcard:*fct_*", "wildcard:*dim_*"],
    target="mermaid",
    artifacts_dir=f"{GITHUB_WORKSPACE}/{NSW_DOE_DATA_STACK_IN_A_BOX_DBT_PROJECT_DIR}",
).get_erd()
# %%
filtered_result = filter_lines(erd)
final = filtered_result.replace("MODEL.NSW_DOE_DATA_STACK_IN_A_BOX.", "")


erd_prep = f"""
```mermaid
---
title: Dimensional ERD
---
{final}
```
"""

# %%
# Write the filtered result to a Markdown file
with open("./ERD.md", "w") as f:
    f.write(erd_prep)
