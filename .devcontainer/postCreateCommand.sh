python3 -m pip install uv
uv venv
. .venv/bin/activate
uv pip install -r requirements.txt 
cd transformation/transformation_nsw_doe && dbt deps
cd ../..
cd orchestration && uv pip install -e ".[dev]"