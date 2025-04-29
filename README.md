Sure! Here's a professionally rewritten and polished version of your **`md2all`** documentation, designed to feel like official open-source documentation:

---

# 📝 md2all

A lightweight Python package to convert Markdown files into beautiful, responsive **HTML** or **PDF** documents—styled with **Tailwind CSS**, **MathJax**, and optimized for clean typography.

> Ideal for note-taking, documentation, and publishing Markdown content without relying on external CDN access.

![PyPI](https://img.shields.io/pypi/v/md2all)  
![Python Version](https://img.shields.io/pypi/pyversions/md2all)  
![License](https://img.shields.io/github/license/codeperfectplus/md2all)

---

## 🚀 Features

- ✅ Convert `.md` files into clean **HTML** or **PDF**
- 🎨 Styled using **Tailwind CSS**
- 🧮 Built-in **MathJax** support for LaTeX equations
- 📝 Beautiful, readable typography with prose class
- 📦 Works offline — no internet or CDN required
- 🔄 Support for CLI 

---

## 🛠️ System Dependencies

To generate PDFs via **Playwright**, some system libraries must be installed.

### On **Debian/Ubuntu**:

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

### On **Fedora/CentOS/RHEL**:

```bash
sudo dnf install -y \
    gstreamer1-plugins-base \
    gstreamer1-plugins-good \
    gstreamer1-plugins-bad-free \
    gstreamer1-libav \
    libavif
```

---

## 📦 Installation

Install `md2all` using `pip`:

```bash
pip install md2all
```

---

## 🖼️ Screenshots

> See `test_data/` for example Markdown and the output.

![Screenshot](test_data/screenshot.png)

---

## ✨ Library Usage

### Function: `convert_markdown`

Convert a Markdown file to **HTML** or **PDF** with optional offline/online resource support.

#### 📥 Parameters

| Parameter       | Type   | Description                                                                 |
|-----------------|--------|-----------------------------------------------------------------------------|
| `md_path`       | `str`  | Path to the Markdown file (relative or absolute).                           |
| `output_dir`    | `str`  | *(Optional)* Directory to save the output. Defaults to the input file's directory. |
| `output_format` | `str`  | *(Optional)* `"html"` or `"pdf"` format. Default is `"pdf"`.                |
| `use_cdn`       | `bool` | *(Optional)* If `True`, loads Tailwind and MathJax via CDN. Default is `False`. |

#### 📤 Returns

- `str`: Full path to the converted file.

---

### ✅ Sync Example (Recommended for most users)

```python
from md2all import convert_markdown

# Convert to HTML
convert_markdown("test_data/test.md", output_format="html")

# Convert to PDF
convert_markdown("test_data/test.md", output_format="pdf")
```

---

### ⚡ Async Example (Ideal for batch/API usage)

```python
import asyncio
from md2all import convert_markdown

async def convert_all():
    await convert_markdown("test_data/test.md", output_format="html")
    await convert_markdown("test_data/test.md", output_format="pdf")

asyncio.run(convert_all())
```

---

## 🧪 Command Line Interface

After installation, the CLI command `md2all` is available globally.

### 📌 Basic Syntax

```bash
md2all -m <md_path> -f <format> [options]
```

### 🎯 Parameters

| Flag                 | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `-m`, `--md_path`    | Path to the input Markdown file. _(Required)_                               |
| `-f`, `--format`     | Output format: `"html"` or `"pdf"`. _(Required)_                            |
| `-o`, `--output_dir` | *(Optional)* Output directory. Defaults to the input file’s folder.         |
| `-c`, `--use_cdn`    | *(Optional)* Use CDN for Tailwind and MathJax. Defaults to offline.         |

---

### 📘 CLI Examples

#### Convert to HTML:

```bash
md2all -m notes/readme.md -f html
```

#### Convert to PDF in a custom directory:

```bash
md2all -m notes/readme.md -f pdf -o ./exports
```

#### Use CDN for styles and MathJax:

```bash
md2all -m notes/readme.md -f pdf -c
```

---

## 📁 Output Structure

- Outputs `.html` or `.pdf` file to your chosen directory.
- Automatically includes all required styling and MathJax configuration.
- Offline assets (CSS/JS) are stored under `~/.lib/`.

---

## 🧑‍💻 Author

**Deepak Raj**  
[GitHub – codeperfectplus](https://github.com/codeperfectplus)

---

## 🤔 Why `md2all`?

> I built `md2all` to make Markdown publishing easier—especially on systems without internet access. With a built-in offline mode, it's ideal for generating clean documents on secure or offline environments.

---

## 💬 Contributions Welcome!

This is an open-source project. Found a bug or want a feature?  
Feel free to open an issue or pull request.
