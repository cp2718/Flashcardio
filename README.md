# Flashcardio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A Python utility for generating printable flashcards from CSV or ODS files with terms and definitions.

## 📖 Overview

**Flashcardio** transforms terms and definitions into perfectly-aligned double-sided flashcards ready for printing.

Each page contains a grid of terms or definitions. After printing (using the "flip on short edge" option), simply cut along the grid lines to create individual flashcards—each with a term on one side and its definition on the reverse.

## ✨ Features

- **Multiple Input Formats:** Process CSV files or ODS spreadsheets (with multiple sheets)
- **Double-Sided Printing:** Creates alternating pages with terms and mirrored definitions
- **Customizable Layout:** Configure columns, rows, and margins to fit your needs
- **Multiple Topics Support:** Each CSV file or ODS sheet becomes a separate section
- **Dynamic Text Sizing:** Automatically adjusts text to fit within each flashcard cell

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Flashcardio.git
   cd Flashcardio
   ```

2. Install required dependencies:
   ```bash
   pip install reportlab odfpy
   ```

## 📋 Input Formats

### CSV Format

Each CSV file should have:
- A header row (will be skipped)
- Two columns: first column for terms, second column for definitions

| Word | Definition |
|------|------------|
| acknowledgment | A formal declaration made before an authorized official. |
| contract | A legally binding agreement between two or more parties. |

### ODS Format

Each sheet in the ODS file should have:
- A header row: "Word", "Definition"
- 2 columns: first for terms, second for definitions

Each sheet will become a separate section in the PDF.

### Sample Files
Check the `samples` folder for examples of a CSV or ODS file with words and definitions.

## 🔧 Usage

### Basic Usage

Running the script without arguments will display the usage help:

```bash
python flashcardio.py
```

This will show:
```
usage: flashcardio.py [-h] [--csv_dir CSV_DIR] [--csv CSV] [--ods ODS] [--output OUTPUT] [--cols COLS] [--rows ROWS] [--margin MARGIN]
```

### Common Commands

Process all CSV files in a directory:
```bash
python flashcardio.py --csv_dir csv_files --output flashcards.pdf
```

Process a single CSV file:
```bash
python flashcardio.py --csv samples/sample.csv --output flashcards.pdf
```

Process an ODS file (each sheet becomes a section):
```bash
python flashcardio.py --ods samples/sample.ods --output flashcards.pdf
```

Combine ODS and CSV sources:
```bash
python flashcardio.py --ods samples/sample.ods --csv_dir csv_files --output combined.pdf
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--csv_dir` | Directory containing CSV files | csv_files |
| `--csv` | Path to a single CSV file | - |
| `--ods` | Path to an ODS file | - |
| `--output` | Output PDF file path | output_table_layout.pdf |
| `--cols` | Number of columns per page | 3 |
| `--rows` | Number of rows per page | 3 |
| `--margin` | Margin size in points (1/72 inch) | 36 |

### Additional Examples

```bash
# Use 4 rows (12 cards per page)
python flashcardio.py --rows 4

# Use custom CSV directory
python flashcardio.py --csv_dir my_csv_folder

# Change column count
python flashcardio.py --cols 4 --rows 2
```

## 🖨️ Printing Instructions

1. Print the generated PDF using double-sided printing
2. Select the "Flip on short edge" option for proper alignment
3. Cut along the grid lines to create individual flashcards
4. Each card will have a term on one side and its definition on the reverse

## 📄 PDF Structure

For each CSV file or ODS sheet:
1. Title page (CSV filename or sheet name, formatted)
2. Words page (batch 1)
3. Definitions page (batch 1, mirrored for double-sided printing)
4. Words page (batch 2)
5. Definitions page (batch 2)
6. ... and so on until all terms are processed

## ⚙️ Requirements

- Python 3.6+
- reportlab (`pip install reportlab`)
- odfpy (`pip install odfpy`) — only needed for ODS file support

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.