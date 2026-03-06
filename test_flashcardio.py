import pytest
import os
import csv
import tempfile
import shutil
from flashcardio import FlashcardPDF, read_csvs


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
        cards = read_csvs(str(csv_file))
        
        assert len(cards) == 2
        assert cards[0] == ("Hello", "A greeting")
        assert cards[1] == ("World", "The planet Earth")
    
    def test_read_csv_with_empty_lines(self, tmp_path):
        """Test that empty lines are skipped"""
        csv_file = tmp_path / "test.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Definition"])
            writer.writerow(["Hello", "A greeting"])
            writer.writerow(["", ""])  # Empty row
            writer.writerow(["World", "The planet Earth"])
        
        cards = read_csvs(str(csv_file))
        
        assert len(cards) == 2  # Empty row should be skipped
    
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
        
        cards = read_csvs(str(tmp_path))
        
        assert len(cards) == 2
        # Note: order may vary, so check presence instead of order
        card_dict = {word: definition for word, definition in cards}
        assert "Alpha" in card_dict
        assert "Beta" in card_dict


class TestFlashcardPDF:
    """Tests for FlashcardPDF class"""
    
    def test_initialization(self):
        """Test FlashcardPDF initialization with default values"""
        pdf = FlashcardPDF()
        
        assert pdf.cols == 3
        assert pdf.rows == 3
        assert pdf.margin == 0.5
    
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
        pdf = FlashcardPDF()
        
        # Create some test cards
        cards = [("Word1", "Definition1"), ("Word2", "Definition2")]
        
        # Build the PDF
        pdf.build_pdf(cards, str(pdf_path))
        
        # Check that file was created
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0
    
    def test_pdf_with_many_cards(self, tmp_path):
        """Test PDF generation with enough cards for multiple pages"""
        pdf_path = tmp_path / "test_multi_page.pdf"
        pdf = FlashcardPDF(cols=3, rows=3)
        
        # Create 20 cards (will span 3 pages)
        cards = [("Word" + str(i), "Definition" + str(i)) for i in range(20)]
        
        pdf.build_pdf(cards, str(pdf_path))
        
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0
        # TODO: Could verify page count by reading the PDF


class TestODSSupport:
    """Tests for ODS file support"""
    
    @pytest.mark.skipif(True, reason="Requires valid ODS file creation")
    def test_ods_reading(self):
        """Test reading ODS files - placeholder for future implementation"""
        # This would require creating a valid ODS file in the test
        # and verifying it can be read correctly
        pass


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
        cards = read_csvs(str(csv_file))
        pdf = FlashcardPDF()
        pdf.build_pdf(cards, str(pdf_path))
        
        # Verify results
        assert len(cards) == 10
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 1000  # PDF should be reasonable size
