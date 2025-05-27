# Flashcardio

A Python utility for generating printable flashcards from CSV files with terms and definitions.

**Workflow:**
This tool generates a PDF where each page contains a grid of words or definitions, perfectly arranged for double-sided printing. After printing (using the “flip on short edge” option), simply cut along the grid lines to create individual flashcards—each with a term on one side and its definition on the reverse.

## Features

- **CSV to PDF Conversion:** Transforms CSV files with terms and definitions into printable flashcards.
- **Double-Sided Printing Support:** Creates alternating pages with words and mirrored definitions for perfect double-sided printing.
- **Customizable Layout:** Configure columns, rows, and margins to fit your needs.
- **Multiple Topics Support:** Processes all CSV files in a directory, creating separate sections with title pages.
- **Dynamic Text Sizing:** Automatically adjusts text to fit within each flashcard cell.

## Requirements

- Python 3.x
- reportlab (`pip install reportlab`)
- odfpy (`pip install odfpy`) - only needed for ODS file support

## Installation

1. Clone this repository or download the source files:
   ```bash
   git clone https://github.com/yourusername/Flashcardio.git
   cd Flashcardio
   ```

2. Install required dependencies:
   ```bash
   pip install reportlab
   ```

## CSV Format

Each CSV file should have:
- A header row (will be skipped)
- Two columns: first column for terms, second column for definitions

Example:
```csv
Word,Definition
acknowledgment,A formal declaration made before an authorized official.
contract,A legally binding agreement between two or more parties.
```

## Usage

### Basic Usage

Running the script without arguments will display the usage help:

```bash
python flashcardio.py
```

This will show:
```
usage: flashcardio.py [-h] [--csv_dir CSV_DIR] [--csv CSV] [--output OUTPUT] [--cols COLS] [--rows ROWS] [--margin MARGIN]
```

To generate flashcards from all CSV files in a folder (default: `csv_files`):

```bash
python flashcardio.py --csv_dir csv_files --output output_table_layout.pdf
```

To generate flashcards from a single CSV file:

```bash
python flashcardio.py file.csv --output output.pdf
```

Or, using the explicit flag:

```bash
python flashcardio.py --csv file.csv --output output.pdf
```

This will create a PDF with flashcards from the specified CSV file.

To generate flashcards from an OpenDocument Spreadsheet (ODS) file:

```bash
python flashcardio.py --ods myfile.ods --output output.pdf
```

To combine an ODS file and a folder of CSVs in one PDF:

```bash
python flashcardio.py --ods myfile.ods --csv_dir csv_files --output output.pdf
```

### Command Line Options

```
usage: flashcardio.py [-h] [--csv_dir CSV_DIR] [--csv CSV] [--ods ODS] [--output OUTPUT] [--cols COLS] [--rows ROWS] [--margin MARGIN]
```

- `--csv_dir`: Directory containing CSV files (default: csv_files)
- `--csv`: Path to a single CSV file
- `--ods`: Path to an OpenDocument Spreadsheet (ODS) file (each sheet becomes a section)
- `--output`: Output PDF file path (default: output_table_layout.pdf)
- `--cols`: Number of columns per page (default: 3)
- `--rows`: Number of rows per page (default: 3, for 9 cards per page)
- `--margin`: Margin size in points, 1/72 inch (default: 36)

### Examples

```bash
# Use 4 rows (12 cards per page)
python flashcardio.py --rows 4

# Use custom CSV directory
python flashcardio.py --csv_dir my_csv_folder

# Specify output filename
python flashcardio.py --output my_cards.pdf

# Generate from a single CSV file
python flashcardio.py my_flashcards.csv --output my_flashcards.pdf

# Generate from an ODS file
python flashcardio.py --ods flashcards.ods --output flashcards.pdf

# Combine ODS and CSV sources
python flashcardio.py --ods flashcards.ods --csv_dir csv_files --output combined.pdf
```

## Printing Instructions

1. Print the generated PDF using double-sided printing.
2. Select the “Flip on short edge” option for double-sided printing to ensure correct alignment.
3. Cut along the grid lines to create individual flashcards.
4. Each card will have a term on one side and its definition on the reverse.

## PDF Structure

For each CSV file:
1. Title page (CSV filename, formatted)
2. Words page (batch 1)
3. Definitions page (batch 1, mirrored for double-sided printing)
4. Words page (batch 2)
5. Definitions page (batch 2)
6. ... and so on until all terms are processed

## License

[Insert your license information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.