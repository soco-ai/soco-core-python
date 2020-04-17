import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.14'
setuptools.setup(
    name="soco-core-python",
    version=VERSION,
    author="tinachez",
    description="Python SDK for using SOCO platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'nltk >= 3.4',
        'tqdm >= 4.32.1'
    ]
)