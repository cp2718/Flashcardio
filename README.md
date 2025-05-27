# Flashcardio

Flashcardio is a Python tool for generating printable flashcards in PDF format from real estate study materials. It supports both OpenDocument Spreadsheet (ODS) and CSV input, and can convert ODS files to CSV before generating the flashcards PDF.

---

## Features

- **ODS to CSV Conversion:** Extracts terms and definitions from each sheet in an ODS file and saves them as separate CSV files.
- **CSV to PDF Flashcards:** Combines all CSV files into a single PDF, formatting each term and definition as a double-sided flashcard (front: term, back: definition).
- **Dynamic Font Sizing:** Automatically adjusts font size to fit content within each flashcard cell.
- **Grid Layout:** Arranges flashcards in a 3x4 grid per page for easy cutting and double-sided printing.
- **Mirrored Backs:** Ensures definitions align with terms for proper double-sided printing.

---

## Project Structure

```
flashcardio.py            # Main entry point: runs ODS-to-CSV and CSV-to-PDF
ods_2_csv.py              # Extracts terms/definitions from ODS to CSVs
csv_2_flashcard.py        # Converts CSVs to PDF flashcards
csv_2_flashcard.bak.py    # Backup/older version of the CSV to PDF script
csv_files/                # Output directory for generated CSVs
ods_files/                # Input directory for ODS files
Flashcards_Real_Estate.pdf  # Example output PDF
```

---

## Requirements

- Python 3.x
- [reportlab](https://pypi.org/project/reportlab/)
- [odfpy](https://pypi.org/project/odfpy/)

Install dependencies with:

```sh
pip install reportlab odfpy
```

---

## Usage

### 1. Run the Full Pipeline (ODS → CSV → PDF)

Place your ODS file (e.g., `Flashcards_Real_Estate.ods`) in the `ods_files/` directory.

Run:

```sh
python flashcardio.py
```

This will:
- Convert the ODS file to CSVs in `csv_files/`
- Generate a PDF (`Flashcards_Real_Estate.pdf`) with all flashcards

### 2. Run Individual Steps

**ODS to CSV:**
```sh
python ods_2_csv.py
```

**CSV to PDF:**
```sh
python csv_2_flashcard.py
```

---

## Customization

- To change the grid layout, margins, or font sizes, edit the constants in [`csv_2_flashcard.py`](csv_2_flashcard.py).
- To use a different ODS or output directory, adjust the paths in [`flashcardio.py`](flashcardio.py).

---

## License

MIT License (add your own license as appropriate).

---

**Author:** Your Name  
**Contact:** your.email@example.com