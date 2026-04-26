import pytest
import os
import csv
import tempfile
import shutil
from flashcardio import FlashcardPDF, extract_ods_to_csvs


class TestCSVReading:
    """Tests for CSV file reading functionality"""
    
    def test_read_single_csv(self, tmp_path):
        """Test reading a single CSV file"""
        # Create a test CSV file
        csv_file = tmp_path / "test.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Hello", "A greeting"])
            writer.writerow(["World", "The planet Earth"])
        
        # Read the CSV
        pdf = FlashcardPDF(csv_file=str(csv_file))
        flashcard_sets = pdf.read_csvs()
        
        assert len(flashcard_sets) == 1
        _, words, definitions = flashcard_sets[0]
        assert len(words) == 2
        assert words[0] == "Hello"
        assert definitions[0] == "A greeting"
        assert words[1] == "World"
        assert definitions[1] == "The planet Earth"
    
    def test_read_csv_with_empty_lines(self, tmp_path):
        """Test that empty lines are skipped"""
        csv_file = tmp_path / "test.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Hello", "A greeting"])
            writer.writerow(["", ""])  # Empty row
            writer.writerow(["World", "The planet Earth"])
        
        pdf = FlashcardPDF(csv_file=str(csv_file))
        flashcard_sets = pdf.read_csvs()
        
        assert len(flashcard_sets) == 1
        _, words, definitions = flashcard_sets[0]
        assert len(words) == 2  # Empty row should be skipped

    def test_read_csv_skips_partial_rows(self, tmp_path):
        """Test that rows with only a word or only a definition are skipped"""
        csv_file = tmp_path / "partial.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["OnlyWord", ""])
            writer.writerow(["", "OnlyDefinition"])
            writer.writerow(["Complete", "Pair"])

        pdf = FlashcardPDF(csv_file=str(csv_file))
        flashcard_sets = pdf.read_csvs()

        assert len(flashcard_sets) == 1
        _, words, definitions = flashcard_sets[0]
        assert len(words) == 1
        assert words[0] == "Complete"
        assert definitions[0] == "Pair"

    def test_read_csv_dir_skips_partial_rows(self, tmp_path):
        """Test that partial rows are also skipped when reading from a directory"""
        csv_file = tmp_path / "partial.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["WordOnly", ""])
            writer.writerow(["Good", "Valid pair"])

        pdf = FlashcardPDF(csv_dirs=[str(tmp_path)])
        flashcard_sets = pdf.read_csvs()

        assert len(flashcard_sets) == 1
        _, words, definitions = flashcard_sets[0]
        assert len(words) == 1
        assert words[0] == "Good"
        assert definitions[0] == "Valid pair"
    
    def test_read_multiple_csvs(self, tmp_path):
        """Test reading from multiple CSV files in a directory"""
        # Create multiple CSV files
        csv1 = tmp_path / "file1.csv"
        csv2 = tmp_path / "file2.csv"
        
        with open(csv1, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Alpha", "First Greek letter"])
        
        with open(csv2, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Beta", "Second Greek letter"])
        
        pdf = FlashcardPDF(csv_dirs=[str(tmp_path)])
        flashcard_sets = pdf.read_csvs()
        
        assert len(flashcard_sets) == 2
        # Note: order may vary, so check presence instead of order
        card_dict = {title: (words[0], defs[0]) for title, words, defs in flashcard_sets}
        assert "file1" in card_dict
        assert card_dict["file1"] == ("Alpha", "First Greek letter")
        assert "file2" in card_dict
        assert card_dict["file2"] == ("Beta", "Second Greek letter")


class TestFlashcardPDF:
    """Tests for FlashcardPDF class"""
    
    def test_initialization(self):
        """Test FlashcardPDF initialization with default values"""
        pdf = FlashcardPDF()
        
        assert pdf.cols == 3
        assert pdf.rows == 3
        assert pdf.margin == 36.0
    
    def test_initialization_custom_values(self):
        """Test FlashcardPDF initialization with custom values"""
        pdf = FlashcardPDF(cols=4, rows=2, margin=1.0)
        
        assert pdf.cols == 4
        assert pdf.rows == 2
        assert pdf.margin == 1.0
    
    def test_batching_logic(self):
        """Test that cards are correctly batched based on cols x rows"""
        pdf = FlashcardPDF(cols=3, rows=3)
        cards = [("Word" + str(i), "Def" + str(i)) for i in range(20)]
        
        # Build batches manually to test the logic
        cards_per_page = pdf.cols * pdf.rows  # 9
        num_batches = (len(cards) + cards_per_page - 1) // cards_per_page
        
        assert cards_per_page == 9
        assert num_batches == 3  # 20 cards / 9 per page = 3 pages (2 full, 1 partial)
    
    def test_pdf_generation(self, tmp_path):
        """Test that PDF file is actually created"""
        pdf_path = tmp_path / "test_output.pdf"
        csv_file = tmp_path / "test.csv"
        
        # Create some test cards in a CSV
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Word1", "Definition1"])
            writer.writerow(["Word2", "Definition2"])
            
        pdf = FlashcardPDF(csv_file=str(csv_file), output_pdf_path=str(pdf_path))
        
        # Build the PDF
        pdf.build_pdf()
        
        # Check that file was created
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0
    
    def test_pdf_with_many_cards(self, tmp_path):
        """Test PDF generation with enough cards for multiple pages"""
        pdf_path = tmp_path / "test_multi_page.pdf"
        csv_file = tmp_path / "test_many.csv"
        
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            for i in range(20):
                writer.writerow([f"Word{i}", f"Definition{i}"])
                
        pdf = FlashcardPDF(csv_file=str(csv_file), output_pdf_path=str(pdf_path), cols=3, rows=3)
        
        pdf.build_pdf()
        
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0
        # TODO: Could verify page count by reading the PDF


class TestODSSupport:
    """Tests for ODS file support"""
    
    def test_ods_reading(self, tmp_path):
        """Test reading ODS files by extracting them to CSVs"""
        # Get path to the sample ODS file
        ods_file = os.path.join(os.path.dirname(__file__), "..", "samples", "sample.ods")
        
        # Skip if the file doesn't exist locally during test execution
        if not os.path.exists(ods_file):
            pytest.skip(f"Sample ODS file not found at {ods_file}")
            
        csv_dir = tmp_path / "csvs"
        
        # Extract the ODS
        extracted_files = extract_ods_to_csvs(ods_file, str(csv_dir))
        
        # Output verification
        assert len(extracted_files) > 0
        assert os.path.exists(csv_dir)
        
        # Verify that we can read the resulting CSVs via FlashcardPDF
        pdf = FlashcardPDF(csv_dirs=[str(csv_dir)])
        flashcard_sets = pdf.read_csvs()
        
        assert len(flashcard_sets) == len(extracted_files)
        # Verify first set has items
        assert len(flashcard_sets[0][1]) > 0
        assert len(flashcard_sets[0][2]) > 0


class TestMultipleDirectories:
    """Tests for combining multiple CSV directories"""

    def test_read_from_multiple_directories(self, tmp_path):
        """Test that csv_dirs reads from all directories, not just the first"""
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()

        with open(dir1 / "set_a.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Alpha", "First letter"])

        with open(dir2 / "set_b.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Beta", "Second letter"])

        pdf = FlashcardPDF(csv_dirs=[str(dir1), str(dir2)])
        flashcard_sets = pdf.read_csvs()

        assert len(flashcard_sets) == 2
        titles = {title for title, _, _ in flashcard_sets}
        assert "set a" in titles
        assert "set b" in titles

    def test_multiple_dirs_and_single_file(self, tmp_path):
        """Test combining csv_dirs with a single csv_file"""
        csv_dir = tmp_path / "dir"
        csv_dir.mkdir()

        with open(csv_dir / "from_dir.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["DirWord", "DirDef"])

        single = tmp_path / "single.csv"
        with open(single, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["FileWord", "FileDef"])

        pdf = FlashcardPDF(csv_dirs=[str(csv_dir)], csv_file=str(single))
        flashcard_sets = pdf.read_csvs()

        assert len(flashcard_sets) == 2
        all_words = [w for _, words, _ in flashcard_sets for w in words]
        assert "DirWord" in all_words
        assert "FileWord" in all_words


class TestEndToEnd:
    """End-to-end integration tests"""
    
    def test_csv_to_pdf_workflow(self, tmp_path):
        """Test complete workflow from CSV to PDF"""
        # Create test CSV
        csv_file = tmp_path / "input.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            for i in range(10):
                writer.writerow([f"Term{i}", f"Meaning{i}"])
        
        # Generate PDF
        pdf_path = tmp_path / "output.pdf"
        pdf = FlashcardPDF(csv_file=str(csv_file), output_pdf_path=str(pdf_path))
        flashcard_sets = pdf.read_csvs()
        pdf.build_pdf()
        
        # Verify results
        assert len(flashcard_sets) == 1
        assert len(flashcard_sets[0][1]) == 10  # 10 words
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 1000  # PDF should be reasonable size
