first add what packages you need to `requirements.in`

```bash
uv pip compile requirements.in -o requirements.txt  # Read a requirements.in file.
```

Then start your enviroment
```bash

uv venv
source .venv/bin/activate 
uv pip sync requirements.txt  # Install from a requirements.txt file.

```