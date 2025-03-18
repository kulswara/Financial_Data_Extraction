from pdf2image import convert_from_bytes
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
import os

def detect_tables_in_pdf(pdf_bytes):
    # Convert PDF pages to images
    print(f"Converting PDF to images: {pdf_bytes}")
    images = convert_from_bytes(pdf_bytes)
    
    # Initialize list to store page numbers with tables
    table_pages = []
    
    # Iterate through each page image
    for i, image in enumerate(images):
        page_num = i + 1  # Page numbers are 1-indexed
        print(f"Processing page {page_num}...")
        
        # Convert PIL Image to OpenCV format
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # METHOD 1: OCR-based detection
        # Use OCR to check for table-related keywords
        ocr_data = pytesseract.image_to_data(image, output_type=Output.DICT)
        text = ' '.join(ocr_data['text']).lower()
        
        # Check for financial table indicators
        financial_keywords = ['total', 'amount', 'balance', 'table', 'financial', 
                             'revenue', 'income', 'expense', 'profit', 'loss',
                             'assets', 'liabilities', 'quarter', 'fiscal', 'year']
        
        has_financial_terms = any(keyword in text for keyword in financial_keywords)
        
        # METHOD 2: Image processing based detection
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Find horizontal and vertical lines which may indicate a table
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        
        horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        
        # Find contours in the horizontal and vertical lines
        h_contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        v_contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # If we have both horizontal and vertical lines, it might be a table
        has_table_structure = len(h_contours) > 3 and len(v_contours) > 3
        
        # Combine the results from both methods
        if has_table_structure:
            table_pages.append(page_num)
            print(f"Table detected on page {page_num}")
    
    return table_pages


