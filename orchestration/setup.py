from setuptools import find_packages, setup

setup(
    name="cese_dia_dagster",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dagstermill",
        "papermill-origami>=0.0.8",
        "pandas"
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
            "pytest"
        ]
    },
)