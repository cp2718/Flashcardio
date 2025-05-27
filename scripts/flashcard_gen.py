
from ods_2_csv import sanitize_filename, extract_words_to_csv
from csv_2_flashcard import csv_to_pdf


def main():
    ods_file = "ods_files/Flashcards_Real_Estate.ods"
    output_dir = "csv_files"
    csv_dir = "csv_files"  # Directory containing CSV files
    output_pdf_path = "Flashcards_Real_Estate.pdf"  # Output PDF file path
    
    #Convert csv files to Flashcards in PDF
    extract_words_to_csv(ods_file, output_dir)
    
    #Convert ods to csv files
    csv_to_pdf(csv_dir, output_pdf_path)

if __name__ == "__main__":
    main()
    