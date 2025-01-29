from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="Four Colors",
    version="0.1",
    description="Read out the four most colors in a picture.",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=requirements,
)
