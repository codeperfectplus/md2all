import setuptools
from glob import glob

# Reading the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Reading the list of requirements from the requirements file
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

# Setting up the package
setuptools.setup(
    name="md2all",
    version="0.0.8",
    author="Deepak Raj",
    author_email="deepak008@live.com",
    description="convertor is a simple and easy to use library for converting markdown files to various formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeperfectplus/md2all",
    data_files=[('assets', glob('md2all/libs/*'))],
    keywords=[

    ],
    install_requires=requirements,
    packages=setuptools.find_packages(),
    project_urls={
        "Documentation": "https://md2all.readthedocs.io/en/latest/",
        "Source": "https://github.com/codeperfectplus/md2all",
        "Tracker": "https://github.com/codeperfectplus/md2all/issues"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "md2all=md2all.cli:main",  # Update path as needed
        ],
    },
)