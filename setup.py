from setuptools import setup, find_packages

setup(
    name="p2pnet",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psutil>=5.8.0",
        "numpy>=1.21.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.18.0",
        "pytest-cov>=3.0.0",
        "ruff>=0.3.0",
    ],
    python_requires=">=3.11"
)