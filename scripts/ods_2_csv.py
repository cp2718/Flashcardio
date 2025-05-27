import csv
import os
import logging
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

logging.basicConfig(level=logging.INFO)

def sanitize_filename(name):
    # Sanitize the sheet name to avoid invalid characters in filenames
    return ''.join(e for e in name if e.isalnum() or e == '_')

def extract_words_to_csv(ods_path, output_dir):
    try:
        doc = load(ods_path)
    except Exception as e:
        logging.error(f"Error opening ODS file: {e}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"📄 Successfully opened ODS file: {ods_path}")
    
    sheets = doc.getElementsByType(Table)
    logging.info(f"Found {len(sheets)} sheet(s) in the ODS file.")
    
    for sheet_idx, sheet in enumerate(sheets):
        sheet_name = sanitize_filename(sheet.getAttribute('name'))
        output_csv_path = os.path.join(output_dir, f"{sheet_name}.csv")
        
        data = []
        logging.info(f"\nProcessing sheet {sheet_idx + 1}/{len(sheets)}: {sheet_name}")
        
        rows = sheet.getElementsByType(TableRow)
        for row_idx, row in enumerate(rows):
            cells = row.getElementsByType(TableCell)
            if len(cells) >= 2:
                word = ''.join([str(p) for p in cells[0].getElementsByType(P)]).strip()
                definition = ''.join([str(p) for p in cells[1].getElementsByType(P)]).strip()
                
                if word:
                    data.append([word, definition])
            else:
                logging.warning(f"⚠️ Row {row_idx + 1} in sheet '{sheet_name}' does not have a valid word, skipping.")
        
        if data:
            try:
                with open(output_csv_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Word', 'Definition'])
                    writer.writerows(data)
                logging.info(f"💾 {sheet_name} saved to {output_csv_path}")
            except Exception as e:
                logging.error(f"Error writing to CSV for sheet '{sheet_name}': {e}")
        else:
            logging.warning(f"⚠️ No valid words found in sheet '{sheet_name}', skipping.")

def main():
    ods_file = "Flashcards_Real_Estate.ods"
    output_dir = "csv_files"
    extract_words_to_csv(ods_file, output_dir)

if __name__ == "__main__":
    main()
