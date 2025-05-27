# csv_2_flashcard.py (updated)

import os
import csv
import math
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# --- Feature Flags ---
ENABLE_DYNAMIC_FONT = True
ENABLE_CELL_LABELS = False  # Removed the index numbers on the definition side

def wrap_text(text, max_width, canvas, font_name="Helvetica", font_size=10):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and canvas.stringWidth(line + words[0], font_name, font_size) <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines

def fit_text_to_box(text, max_width, max_height, canvas, font_name="Helvetica", max_font_size=10, min_font_size=5, line_spacing=1.2):
    font_size = max_font_size
    while font_size >= min_font_size:
        canvas.setFont(font_name, font_size)
        lines = wrap_text(text, max_width, canvas, font_name, font_size)
        total_height = len(lines) * font_size * line_spacing
        if total_height <= max_height:
            return font_size, lines
        font_size -= 1
    canvas.setFont(font_name, min_font_size)
    return min_font_size, wrap_text(text, max_width, canvas, font_name, min_font_size)

def format_title(title):
    return title.replace("_", " ").replace(".csv", "")

def draw_dashed_grid(canvas, width, height, margin, cols, rows):
    cell_width = (width - 2 * margin) / cols
    cell_height = (height - 2 * margin) / rows
    canvas.setDash(3, 3)
    
    # Draw vertical lines
    for col in range(cols + 1):
        x = margin + col * cell_width
        canvas.line(x, margin, x, height - margin)
    
    # Draw horizontal lines
    for row in range(rows + 1):
        y = margin + row * cell_height
        canvas.line(margin, y, width - margin, y)

def csv_to_pdf(csv_dir, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    cols, rows = 3, 4
    cell_width = (width - 2 * margin) / cols
    cell_height = (height - 2 * margin) / rows

    total_words = 0

    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(csv_dir, csv_file)
            words, definitions = [], []
            
            try:
                with open(csv_path, newline='') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        if len(row) >= 2:
                            words.append(row[0])
                            definitions.append(row[1])
            except Exception as e:
                print(f"Failed to read {csv_file}: {e}")
                continue
            
            total_words += len(words)

            title = format_title(csv_file)
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width / 2, height / 2, title)
            c.showPage()

            num_cards = len(words)
            num_pages = math.ceil(num_cards / (cols * rows))

            for page_idx in range(num_pages):
                start = page_idx * cols * rows
                end = start + cols * rows
                page_words = words[start:end]
                page_defs = definitions[start:end]

                # --- Front: Words ---
                draw_dashed_grid(c, width, height, margin, cols, rows)
                for i, word in enumerate(page_words):
                    col = i % cols
                    row = i // cols
                    x = margin + col * cell_width + 0.1 * inch
                    total_height = len(wrap_text(word, cell_width - 0.2 * inch, c)) * 14 * 1.2
                    y = height - margin - (row + 1) * cell_height + (cell_height + total_height) / 2 - 14

                    if ENABLE_DYNAMIC_FONT:
                        font_size, wrapped_word = fit_text_to_box(word, cell_width - 0.2 * inch, cell_height - 0.4 * inch, c, font_name="Helvetica-Bold")
                    else:
                        font_size = 14
                        wrapped_word = wrap_text(word, cell_width - 0.2 * inch, c, font_name="Helvetica-Bold", font_size=font_size)
                        c.setFont("Helvetica-Bold", font_size)

                    c.setFont("Helvetica-Bold", font_size)
                    for line in wrapped_word:
                        c.drawString(x, y, line)
                        y -= font_size * 1.2

                c.showPage()

                # --- Back: Definitions (mirrored) ---
                draw_dashed_grid(c, width, height, margin, cols, rows)
                for i, definition in enumerate(page_defs):
                    col = (cols - 1) - (i % cols)
                    row = i // cols
                    x = margin + col * cell_width + 0.1 * inch
                    
                    # Calculate available space for the definition
                    available_height = cell_height - 0.4 * inch
                    total_height = len(wrap_text(definition, cell_width - 0.2 * inch, c)) * 10 * 1.2
                    y = height - margin - (row + 1) * cell_height + (available_height + total_height) / 2 - 10

                    if ENABLE_DYNAMIC_FONT:
                        font_size, wrapped_text = fit_text_to_box(definition, cell_width - 0.2 * inch, available_height, c)
                    else:
                        font_size = 10
                        wrapped_text = wrap_text(definition, cell_width - 0.2 * inch, c, font_size=font_size)
                        c.setFont("Helvetica", font_size)

                    c.setFont("Helvetica", font_size)
                    for line in wrapped_text:
                        c.drawString(x, y, line)
                        y -= font_size * 1.2

                c.showPage()

    c.save()
    print(f"Total number of words made into flashcards: {total_words}")

def main():
    # Specify the directory where your CSV files are located
    csv_dir = "csv_files"  # Adjust to your CSV folder path
    output_pdf_path = "output.pdf"  # Specify your output PDF file path
    
    # Call the function to convert CSV files to PDF
    csv_to_pdf(csv_dir, output_pdf_path)

if __name__ == "__main__":
    main()
