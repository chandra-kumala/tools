import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="wagtail-reusable-tools",
    version="0.0.1",
    description="Streamfields, blocks, and templates for basic features.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chandra-kumala-school/tools",
    author="Simon Holland (aka Inyoka)",
    author_email="simonmarkholland@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[""],
)
