import os
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import math

def wrap_text(text, max_width, canvas, font_name="Helvetica", font_size=10):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and canvas.stringWidth(line + words[0], font_name, font_size) <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines

def format_title(title):
    return title.replace("_", " ").replace(".csv", "")

def csv_to_pdf(csv_dir, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch  # Small margin around the page
    cols, rows = 3, 4
    cell_width = (width - 2 * margin) / cols
    cell_height = (height - 2 * margin) / rows

    total_words = 0

    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(csv_dir, csv_file)
            words = []
            definitions = []
            
            with open(csv_path, newline='') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 2:
                        words.append(row[0])
                        definitions.append(row[1])
            
            total_words += len(words)
            
            # Title Page
            title = format_title(csv_file)
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width / 2, height / 2, title)
            c.showPage()

            # Flashcard Pages (front = word, back = definition)
            num_cards = len(words)
            num_pages = math.ceil(num_cards / (cols * rows))

            for page_idx in range(num_pages):
                start = page_idx * cols * rows
                end = start + cols * rows
                page_words = words[start:end]
                page_defs = definitions[start:end]

                # Front - words
                for i, word in enumerate(page_words):
                    col = i % cols
                    row = i // cols
                    x = margin + col * cell_width + 0.1 * inch
                    y = height - margin - (row + 1) * cell_height + 0.3 * inch
                    c.setFont("Helvetica-Bold", 14)
                    wrapped_word = wrap_text(word, cell_width - 0.2 * inch, c, font_name="Helvetica-Bold", font_size=14)
                    for line in wrapped_word:
                        c.drawString(x, y, line)
                        y -= 14

                c.showPage()

                # Back - definitions (mirrored to match front layout for double-sided print)
                for i, definition in enumerate(page_defs):
                    col = (cols - 1) - (i % cols)
                    row = i // cols
                    x = margin + col * cell_width + 0.1 * inch
                    y = height - margin - (row + 1) * cell_height + 0.3 * inch
                    c.setFont("Helvetica", 10)
                    wrapped_text = wrap_text(definition, cell_width - 0.2 * inch, c)
                    for line in wrapped_text:
                        c.drawString(x, y, line)
                        y -= 12

                c.showPage()

    c.save()
    
    print(f"Total number of words made into flashcards: {total_words}")

def main():
    csv_dir = "csv_files"  # Directory containing CSV files
    output_pdf_path = "flashcards_output.pdf"  # Output PDF file path
    csv_to_pdf(csv_dir, output_pdf_path)

if __name__ == "__main__":
    main()
