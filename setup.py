from setuptools import setup, find_packages

setup(
    name="Agentic_Trader",
    version="1.1.0",
    description="AI agent for debating trading choices on the Pakistan Stock Exchange (PSX)",
    author="Saad Waseem",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "tqdm",
        "selenium",
        "beautifulsoup4",
        "requests",
        "python-dotenv"
    ],
    python_requires=">=3.7",
)