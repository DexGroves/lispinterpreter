from setuptools import setup, find_packages

setup(
    name="lispinterpreter",
    version="0.1",
    description="Trying to do that leetcode problem",
    url="TODO",
    author="Declan Groves",
    license="GPL 2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    setup_requires=["pytest-runner",],
)
