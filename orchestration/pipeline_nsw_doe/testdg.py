import time
import os
import re


os.environ["TEST_BRANCH"] = "bug/Dave-yea"
print(os.getenv("TEST_BRANCH"))

# load_dotenv()

# work around to set schema when in a branch deployment, TEST_BRANCH is only present in branch deployments
if "TEST_BRANCH" in os.environ:
    # Get the current timestamp
    timestamp = int(time.time())
    pr_string = f"pr_{timestamp}_"

    # Get the Git branch (assuming it's an environment variable)
    git_branch = os.environ.get("TEST_BRANCH", "")
    git_branch_lower = git_branch.lower()

    # Replace non-alphanumeric characters with underscores
    git_branch_clean = re.sub(r"[^a-zA-Z0-9]", "_", git_branch_lower)

    # Final result
    result = pr_string + git_branch_clean
    print(f"setting NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA = {result}")
    os.environ["NSW_DOE_DATA_STACK_IN_A_BOX_TARGET_SCHEMA"] = result
