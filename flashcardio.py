from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import csv
import math
import argparse
import tempfile
import shutil
import re
import sys

class FlashcardPDF:
    def __init__(self, csv_dir=None, csv_file=None, output_pdf_path='output.pdf', cols=3, rows=3, margin=36):
        self.csv_dir = csv_dir
        self.csv_file = csv_file
        self.output_pdf_path = output_pdf_path
        self.cols = cols
        self.rows = rows
        self.margin = margin
        self.page_width, self.page_height = letter
        
        # Styles for words and definitions
        self.word_style = ParagraphStyle('Word', fontName='Helvetica-Bold', fontSize=14, 
                                         alignment=TA_CENTER, leading=16)
        self.def_style = ParagraphStyle('Def', fontName='Helvetica', fontSize=10, 
                                        alignment=TA_CENTER, leading=12)

    def read_csvs(self):
        """Read all CSV files from sources and return a list of (title, words, definitions)."""
        flashcard_sets = []
        
        # Process single CSV file if provided
        if self.csv_file and os.path.exists(self.csv_file):
            words, definitions = [], []
            with open(self.csv_file, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        words.append(row[0])
                        definitions.append(row[1])
            title = os.path.basename(self.csv_file).replace('_', ' ').replace('.csv', '')
            flashcard_sets.append((title, words, definitions))
        
        # Process CSV directory if provided
        if self.csv_dir and os.path.exists(self.csv_dir):
            csv_files = sorted([f for f in os.listdir(self.csv_dir) if f.endswith('.csv')])
            for csv_file in csv_files:
                file_path = os.path.join(self.csv_dir, csv_file)
                words, definitions = [], []
                try:
                    with open(file_path, newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        next(reader)  # Skip header
                        for row in reader:
                            if len(row) >= 2:
                                words.append(row[0])
                                definitions.append(row[1])
                    title = csv_file.replace('_', ' ').replace('.csv', '')
                    flashcard_sets.append((title, words, definitions))
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
                
        return flashcard_sets

    def build_pdf(self):
        """Build the PDF with strictly alternating pages: title, words, definitions, words, definitions..."""
        c = canvas.Canvas(self.output_pdf_path, pagesize=letter)
        flashcard_sets = self.read_csvs()
        
        for title, words, definitions in flashcard_sets:
            # Add title page
            self.add_title_page(c, title)
            c.showPage()  # End the page
            
            # Calculate cards per page and batches
            cards_per_page = self.cols * self.rows
            num_batches = math.ceil(len(words) / cards_per_page)
            
            for batch_idx in range(num_batches):
                start = batch_idx * cards_per_page
                end = min(start + cards_per_page, len(words))
                
                # Words page
                batch_words = words[start:end]
                self.draw_flashcard_grid(c, batch_words, is_definition=False)
                c.showPage()  # End the page
                
                # Definitions page (mirrored)
                batch_defs = definitions[start:end]
                self.draw_flashcard_grid(c, batch_defs, is_definition=True, mirror=True)
                c.showPage()  # End the page
        
        c.save()

    def add_title_page(self, canvas, title):
        """Add a title page to the PDF."""
        canvas.setFont("Helvetica-Bold", 24)
        title_width = canvas.stringWidth(title, "Helvetica-Bold", 24)
        x = (self.page_width - title_width) / 2
        y = self.page_height / 2
        canvas.drawString(x, y, title)

    def draw_flashcard_grid(self, canvas, items, is_definition=False, mirror=False):
        """Draw a grid of flashcards on the canvas."""
        # Calculate cell dimensions
        cell_width = (self.page_width - 2 * self.margin) / self.cols
        cell_height = (self.page_height - 2 * self.margin) / self.rows
        
        # Extend items list to fill the grid
        cards_per_page = self.cols * self.rows
        items = list(items) + [''] * (cards_per_page - len(items))
        
        # Draw grid
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate cell position
                x = self.margin + col * cell_width
                y = self.page_height - self.margin - (row + 1) * cell_height
                
                # Determine cell index based on mirroring
                if mirror and is_definition:
                    idx = row * self.cols + (self.cols - 1 - col)
                else:
                    idx = row * self.cols + col
                
                if idx < len(items):
                    text = items[idx]
                    # Draw cell border
                    canvas.rect(x, y, cell_width, cell_height)
                    
                    # Draw text in cell
                    self.draw_text_in_cell(canvas, text, x, y, cell_width, cell_height, is_definition)

    def draw_text_in_cell(self, canvas, text, x, y, width, height, is_definition):
        """Draw text centered in a cell with appropriate wrapping."""
        if not text:
            return
            
        # Use smaller font for definitions
        style = self.def_style if is_definition else self.word_style
        
        # Create paragraph for wrapping
        p = Paragraph(text.replace('\n', '<br/>'), style)
        
        # Get available space
        avail_width = width - 12  # Account for padding
        avail_height = height - 12
        
        # Get paragraph dimensions
        w, h = p.wrap(avail_width, avail_height)
        
        # Draw the paragraph centered in the cell
        p_x = x + (width - w) / 2
        p_y = y + (height - h) / 2
        p.drawOn(canvas, p_x, p_y)

def extract_ods_to_csvs(ods_path, output_dir):
    """Extract sheets from an ODS file to individual CSV files."""
    try:
        from odf.opendocument import load
        from odf.table import Table, TableRow, TableCell
        from odf.text import P
    except ImportError:
        print("Error: odfpy library not found. Please install it with: pip install odfpy")
        sys.exit(1)
        
    # Load the ODS file
    try:
        doc = load(ods_path)
        tables = doc.getElementsByType(Table)
    except Exception as e:
        print(f"Error loading ODS file {ods_path}: {str(e)}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    extracted_files = []
    
    for table in tables:
        table_name = table.getAttribute("name")
        if not table_name:
            continue
            
        # Sanitize table name for filename
        filename = sanitize_filename(table_name) + ".csv"
        output_path = os.path.join(output_dir, filename)
        
        # Extract rows and cells
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Word", "Definition"])  # Header
            
            rows = table.getElementsByType(TableRow)
            for row_idx, row in enumerate(rows):
                if row_idx == 0:  # Skip header row
                    continue
                    
                cells = row.getElementsByType(TableCell)
                if len(cells) >= 2:
                    word = get_cell_text(cells[0])
                    definition = get_cell_text(cells[1])
                    if word and definition:  # Only write if both word and definition exist
                        writer.writerow([word, definition])
        
        extracted_files.append(output_path)
        print(f"Extracted sheet '{table_name}' to {output_path}")
        
    return extracted_files

def sanitize_filename(name):
    """Replace spaces and special chars with underscores."""
    return re.sub(r'[^\w\-_.]', '_', name)
    
def get_cell_text(cell):
    """Extract text from a cell."""
    from odf.text import P
    text_nodes = cell.getElementsByType(P)
    return " ".join(node.firstChild.data if node.firstChild else "" for node in text_nodes)

def main():
    parser = argparse.ArgumentParser(description="Generate flashcard PDF from CSV or ODS files.")
    parser.add_argument('csv_file', nargs='?', type=str, help='Path to a single CSV file')
    parser.add_argument('--csv', type=str, help='Path to a single CSV file')
    parser.add_argument('--csv_dir', type=str, help='Directory containing CSV files')
    parser.add_argument('--ods', type=str, help='Path to an ODS file with multiple sheets')
    parser.add_argument('--output', type=str, default='output_table_layout.pdf', help='Output PDF file path')
    parser.add_argument('--cols', type=int, default=3, help='Number of columns per page')
    parser.add_argument('--rows', type=int, default=3, help='Number of rows per page (default: 3, for 9 cards per page)')
    parser.add_argument('--margin', type=int, default=36, help='Margin size in points (1/72 inch)')
    
    args = parser.parse_args()
    
    # Determine the CSV file (from either --csv or positional argument)
    csv_file = args.csv or args.csv_file
    
    # If no arguments provided, just print usage and exit
    if not args.csv_dir and not csv_file and not args.ods:
        parser.print_usage()
        return
        
    csv_dirs = []
    temp_dir = None
    
    try:
        # If ODS file is provided, extract sheets to temp directory
        if args.ods:
            if not os.path.exists(args.ods):
                print(f"Error: ODS file not found: {args.ods}")
                return
                
            print(f"Extracting sheets from {args.ods}...")
            temp_dir = tempfile.mkdtemp(prefix="flashcardio_")
            extract_ods_to_csvs(args.ods, temp_dir)
            csv_dirs.append(temp_dir)
            
        # Add CSV directory if provided
        if args.csv_dir:
            if not os.path.exists(args.csv_dir):
                print(f"Error: CSV directory not found: {args.csv_dir}")
                return
            csv_dirs.append(args.csv_dir)
            
        # Generate the PDF with all sources
        pdf_maker = FlashcardPDF(
            csv_dir=csv_dirs[0] if csv_dirs else None,
            csv_file=csv_file,
            output_pdf_path=args.output,
            cols=args.cols,
            rows=args.rows,
            margin=args.margin
        )
        pdf_maker.build_pdf()
        
        print(f"Flashcards created: {args.output}")
        
    finally:
        # Clean up temp directory if created
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

if __name__ == "__main__":
    main()
