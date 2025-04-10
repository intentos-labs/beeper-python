from setuptools import setup, find_packages

setup(
    name="beeper",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "beeper": ["solc/**/*"],
    },
    install_requires=[
        "web3>=7.10.0",
        "python-dotenv>=1.1.0",
        "requests>=2.26.0",
    ],
    tests_require=[
        "pytest>=8.3.5",
    ],
) 