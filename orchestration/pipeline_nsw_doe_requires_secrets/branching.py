import os
import re


def set_schema_name_env():
    """creates the schema name for the variable NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA"""
    if os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA"):
        """already set as part of environment setup"""
        pass

    # work around to set schema when in a branch deployment, DAGSTER_CLOUD_GIT_BRANCH is only present in branch deployments
    elif (
        "DAGSTER_CLOUD_GIT_BRANCH" in os.environ
        and os.getenv("NSW_DOE_DATA_STACK_IN_A_BOX__ENV") != "prod"
    ):
        # Get the current timestamp
        # timestamp = int(time.time())
        # pr_string = f"pr_{timestamp}_"
        pr_string = "pr_full_"

        # Get the Git branch (assuming it's an environment variable)
        git_branch = os.environ.get("DAGSTER_CLOUD_GIT_BRANCH", "")
        git_branch_lower = git_branch.lower()

        # Replace non-alphanumeric characters with underscores
        git_branch_clean = re.sub(r"[^a-zA-Z0-9]", "_", git_branch_lower)

        # Final result
        result = pr_string + git_branch_clean
        print(f"setting NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA = {result}")
        os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA"] = result
    else:
        os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA"] = "schema_not_set"
