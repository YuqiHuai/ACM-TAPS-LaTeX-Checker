# ACM TAPS LaTeX Checker

**ACM TAPS LaTeX Checker** is a command-line tool that validates LaTeX files against the official [ACM TAPS supported package list](https://authors.acm.org/proceedings/production-information/accepted-latex-packages).

It helps authors ensure their LaTeX submissions comply with ACM TAPS requirements by detecting unsupported packages and duplicate imports that are already loaded by the ACM class file.

---

## ✨ Features

- Recursive directory scanning (enabled by default)
- Ruff-style error output in the form: `file:line: CODE message`
- Deterministic, sorted results (stable for CI environments)
- Colored terminal output
- JSON output mode for automation and pipelines
- Clear and structured error codes

---

## 🔎 What It Detects

### TAPS001 — Unsupported Package  
Reports packages that are not included in the official ACM TAPS supported list.

### TAPS002 — Duplicate Package  
Reports packages that are already loaded automatically by the ACM class file and should not be imported manually.

---

## 📦 Installation

Install using Poetry:

```bash
    poetry install
```

Or install into your Python environment:

```bash
    pip install .
```

---

## 🚀 Usage

### Validate a Single File

Run:

```bash
    taps-latex-check paper.tex
```

Example output:

```
    paper.tex:12: TAPS001 Unsupported module ['badpkg']
    paper.tex:15: TAPS002 Duplicate module ['amsmath']
```

---

### Validate a Directory (Recursive by Default)

Run:

```bash
    taps-latex-check .
```

All `.tex` files within the directory tree will be scanned automatically.

---

### JSON Output (for CI Integration)

Run:

```bash
    taps-latex-check . --json
```

Example JSON output:

```json
    {
      "paper.tex": {
        "unsupported": {
          "badpkg": [12]
        },
        "duplicate": {
          "amsmath": [15]
        }
      }
    }
```

---

## 📌 Exit Codes

```
0 — No issues found  
1 — One or more issues detected  
```

---

## 🧠 How It Works

1. Extracts `\usepackage{...}` statements from LaTeX files  
2. Compares them against:
   - `taps_accepted-packages.json` (official supported list)
   - `additional.txt` (packages implicitly loaded by the ACM class)
3. Reports unsupported and duplicate imports  
4. Returns a non-zero exit code if any issues are found  

---

## 🧪 Development

Run tests:

```bash
    poetry run pytest
```

Lint and format:

```bash
    poetry run ruff check . --fix  
    poetry run ruff format .
```

---

## 🏗 Project Structure

```
    src/acm_taps_latex_checker/
        cli.py
        validator.py
        latex_parser.py
        load_local_list.py
        load_additional.py
        data/
            taps_accepted-packages.json
            additional.txt
    tests/
```
