from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the list of requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="md2htmlify",
    version="0.0.1",
    author="Deepak Raj",
    author_email="deepak008@live.com",
    description=(
        "A simple, user-friendly library for converting Markdown files to HTML, "
        "with optional local or CDN-based math and styling dependencies."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeperfectplus/md2htmlify",
    packages=find_packages(),
    # Instead of using data_files, it's often preferable to use package_data
    # or include_package_data to ensure files get included with the package itself.
    # For any non-Python assets, place them in a package directory (e.g. md2htmlify/libs).
    # Example usage: package_data={"md2htmlify": ["libs/*"]},
    # or rely on MANIFEST.in to fine-tune inclusion.
    include_package_data=True,
    package_data={
        "md2htmlify": ["libs/*"]  # Adjust the pattern as needed
    },
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    project_urls={
        "Documentation": "https://md2htmlify.readthedocs.io/en/latest/",
        "Source": "https://github.com/codeperfectplus/md2htmlify",
        "Tracker": "https://github.com/codeperfectplus/md2htmlify/issues"
    },
    entry_points={
        "console_scripts": [
            "md2htmlify=md2htmlify.cli:main",  # Update path if needed
        ],
    },
    keywords=[
        "markdown",
        "html",
        "converter",
        "mathjax",
        "tailwind",
        "latex",
        "documentation",
    ],
    license="MIT",
)