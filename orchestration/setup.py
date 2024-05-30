from setuptools import find_packages, setup
from pathlib import Path


requirements = Path(__file__).parent.joinpath("..", "requirements.txt")

with open(requirements) as f:
    install_requires = f.read().splitlines()

setup(
    name="cese_dia_dagster",
    version="0.0.1",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
