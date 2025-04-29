# 📝 md2all

A minimal Python package to convert Markdown files to clean, responsive **HTML** with **Tailwind CSS**, **MathJax**, and beautiful typography.

> Ideal for note-taking, documentation, and publishing markdown content as styled web pages.

![PyPI](https://img.shields.io/pypi/v/md2all)
![Python Version](https://img.shields.io/pypi/pyversions/md2all)
![License](https://img.shields.io/github/license/codeperfectplus/md2all)

---

## 🚀 Features

- 🧪 Convert `.md` files into HTML
- 🎨 Built-in support for **Tailwind CSS**
- 🧮 Renders LaTeX/Math using **MathJax**
- ✨ Applies prose styling for readability
- 🗂 Outputs to your desired directory

---

## Install Dependencies

#### 🛠️ For **Debian/Ubuntu**:

```bash
sudo apt update
sudo apt install -y \
    libavif13 \
    libgstreamer-plugins-base1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    libgstreamer-plugins-base1.0-dev
```

#### 🛠️ For **CentOS/RHEL/Fedora**:

```bash
sudo dnf install -y \
    gstreamer1-plugins-base \
    gstreamer1-plugins-good \
    gstreamer1-plugins-bad-free \
    gstreamer1-libav \
    libavif
```


## 📦 Installation

```bash
pip install md2all
```

## Screenshots

> Check the test_data for the example mardown file and the output HTML and Pdf files.

![Screenshot](test_data/screenshot.png)

## How to Use it

Sure! Here's a concise and developer-friendly **documentation** for using the `convert_markdown` function as part of your Python library (assuming it's installed from PyPI):

---

## 📄 `convert_markdown`

Convert a Markdown (`.md`) file into a styled HTML file with TailwindCSS and MathJax support.

---

### ✨ Features

- Converts `.md` files to clean, styled **HTML**
- Supports **LaTeX math** using `$$...$$` (rendered via MathJax)
- Automatically applies Tailwind CSS and custom styling
- Resolves relative paths and saves output to the desired directory

---

### 📥 Parameters

| Name            | Type   | Description                                                                 |
|-----------------|--------|-----------------------------------------------------------------------------|
| `md_path`       | str    | Path to the input Markdown file. Can be relative or absolute.               |
| `output_dir`    | str    | *(Optional)* Directory to save the converted file. Defaults to input file's directory. |
| `output_format` | str    | *(Optional)* Set to `"html"` to output HTML. Default is `"pdf"` |
| `use_cdn`   | bool   | *(Optional)* If `True`, uses CDN else use offline resources. Default is `False`.(Useful in case your system deosn't have access to internet) |
---

### 📤 Returns

- Full path to the converted file.

---

### 🧪 Example Usage

#### Sync Code(Good for general usage)

```python
from md2all import convert_markdown

md_path = "test_data/test.md"
convert_markdown(md_path, output_format="html")


md_path = "test_data/test.md"
convert_markdown(md_path, output_format="pdf")
```

#### Async Code(Good for large number of files and API usage)

```python
import asyncio

from md2all import convert_markdown

md_path = "test_data/test.md"

async def convert_to_html():
    """ Convert Markdown to HTML. """
    await convert_markdown(md_path, output_format="html")

async def convert_to_pdf():
    """ Convert Markdown to PDF. """
    await convert_markdown(md_path, output_format="pdf")

asyncio.run(convert_to_html())
asyncio.run(convert_to_pdf())
```


---

### 📁 Output Structure

- create a `.html` file to your specified `output_dir`, if not provided, it will be saved in the same directory as the input file.
- Includes all CSS and MathJax setup in the HTML head section. all css and js library are inside /home/.lib/

---

## Author 

- Deepak Raj

## Why Md2all?

- I created this library to simplify the process of converting Markdown files into styled HTML/PDF documents for the system which doesn't have access to CDN/Internet. So, I made it a standalone library that can be used in any environment without the need for external resources.