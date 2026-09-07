from setuptools import setup, find_packages

setup(
    name="pyhawk",
    version="0.3.1",
    description="PyHawk Programming Language — Sharp as a hawk, fast as math (Python Prototype)",
    author="minnardev",
    packages=find_packages(),
    py_modules=["hawk_cli"],
    package_data={
        "hawk": ["runtime/*.h", "stdlib/*.hwk"],
    },
    entry_points={
        "console_scripts": [
            "pyhawk=hawk_cli:main",
            "hawk=hawk_cli:main",
        ],
    },
    python_requires=">=3.8",
)
