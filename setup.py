from setuptools import find_packages, setup

setup(
    name="flatten",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pyperclip", "pathspec"],
    entry_points={"console_scripts": ["flatten=flatten.cli:main"]},
)
