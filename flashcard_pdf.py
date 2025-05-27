from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
import csv
import math

class FlashcardPDF:
    def __init__(self, csv_dir, output_pdf_path, cols=3, rows=4, margin=36):
        self.csv_dir = csv_dir
        self.output_pdf_path = output_pdf_path
        self.cols = cols
        self.rows = rows
        self.margin = margin
        self.page_width, self.page_height = letter
        self.styles = getSampleStyleSheet()

    def read_csvs(self):
        """Read all CSV files in the directory and return a list of (title, words, definitions)."""
        flashcard_sets = []
        for csv_file in os.listdir(self.csv_dir):
            if csv_file.endswith('.csv'):
                words, definitions = [], []
                with open(os.path.join(self.csv_dir, csv_file), newline='') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        if len(row) >= 2:
                            words.append(row[0])
                            definitions.append(row[1])
                title = csv_file.replace('_', ' ').replace('.csv', '')
                flashcard_sets.append((title, words, definitions))
        return flashcard_sets

    def make_flashcard_table(self, items, is_definition=False, mirror=False):
        """Return a Table object for a single page of flashcards (words or definitions). If mirror=True, each row is reversed (for double-sided printing)."""
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        cards_per_page = self.cols * self.rows
        page_items = list(items)
        while len(page_items) < cards_per_page:
            page_items.append('')
        # Use Paragraph for wrapping
        table_data = []
        # Use a smaller font for definitions
        word_style = ParagraphStyle('Word', fontName='Helvetica-Bold', fontSize=14, alignment=TA_CENTER, leading=16)
        def_style = ParagraphStyle('Def', fontName='Helvetica', fontSize=10, alignment=TA_CENTER, leading=12)
        style = def_style if is_definition else word_style
        for i in range(self.rows):
            row_cells = page_items[i*self.cols:(i+1)*self.cols]
            if mirror:
                row_cells = row_cells[::-1]
            row = [Paragraph(cell.replace('\n', '<br/>'), style) if cell else '' for cell in row_cells]
            table_data.append(row)
        table_style = TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ])
        cell_width = (self.page_width - 2*self.margin) / self.cols
        cell_height = (self.page_height - 2*self.margin) / self.rows
        table = Table(table_data, colWidths=[cell_width]*self.cols, rowHeights=[cell_height]*self.rows, repeatRows=0)
        table.setStyle(table_style)
        return table

    def build_pdf(self):
        doc = SimpleDocTemplate(self.output_pdf_path, pagesize=letter, leftMargin=self.margin, rightMargin=self.margin, topMargin=self.margin, bottomMargin=self.margin)
        elements = []
        for title, words, definitions in self.read_csvs():
            # Title page
            elements.append(Spacer(1, 2*36))
            elements.append(Paragraph(f"<b>{title}</b>", self.styles['Title']))
            elements.append(PageBreak())
            cards_per_page = self.cols * self.rows
            num_pages = math.ceil(len(words) / cards_per_page)
            for page_idx in range(num_pages):
                start = page_idx * cards_per_page
                end = start + cards_per_page
                # Words page
                word_table = self.make_flashcard_table(words[start:end], is_definition=False, mirror=False)
                elements.append(word_table)
                elements.append(PageBreak())
                # Definitions page (mirrored horizontally for double-sided printing)
                def_table = self.make_flashcard_table(definitions[start:end], is_definition=True, mirror=True)
                elements.append(def_table)
                elements.append(PageBreak())
        doc.build(elements)
        print(f"PDF generated: {self.output_pdf_path}")

def main():

    import argparse
    parser = argparse.ArgumentParser(description="Generate flashcard PDF from CSV files.")
    parser.add_argument('--csv_dir', type=str, default='csv_files', help='Directory containing CSV files')
    parser.add_argument('--output', type=str, default='output_table_layout.pdf', help='Output PDF file path')
    parser.add_argument('--cols', type=int, default=3, help='Number of columns per page')
    parser.add_argument('--rows', type=int, default=4, help='Number of rows per page')
    parser.add_argument('--margin', type=int, default=36, help='Margin size in points (1/72 inch)')
    args = parser.parse_args()

    pdf_maker = FlashcardPDF(
        csv_dir=args.csv_dir,
        output_pdf_path=args.output,
        cols=args.cols,
        rows=args.rows,
        margin=args.margin
    )
    pdf_maker.build_pdf()

if __name__ == "__main__":
    main()
