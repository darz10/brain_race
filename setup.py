from setuptools import setup, find_packages

setup(
    name="brain_race",
    version="1.0",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "asyncpg==0.24.0",
        "fastapi==0.70.0",
        "jose==1.0.0",
        "passlib==1.7.4",
        "pydantic==1.8.2",
    ],
    extras_require={
        "dev": [
            "pytest"
        ]
    },
    author="Vedernikov Artem",
    author_email="vedernikov.tema1996@gmail.com",
)