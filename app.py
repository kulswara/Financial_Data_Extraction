import io
import re
import logging
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import streamlit as st
from extractor_engine import detect_tables_in_pdf
from LLM_engine import generate_text_response 
import traceback
import json  # Added json module

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_pdf(file_bytes: bytes, pages_with_tables: list):
    """Process PDF and return extracted text."""
    try:
        doc = fitz.open("pdf", file_bytes)
        all_text = ""
        
        for page_number in pages_with_tables:
            try:
                page = doc[page_number - 1]
                text_direct = page.get_text()
                
                # OCR processing
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                ocr_text = pytesseract.image_to_string(img_data, lang='eng')
                
                page_text = f"\n--- Page {page_number} ---\n{(text_direct + '\n' + ocr_text).strip()}\n"
                all_text += page_text
                
            except Exception as e:
                logger.error(f"Error processing page {page_number}: {str(e)}")
                continue
        
        doc.close()
        return all_text.strip() or None  # Return None if empty
        
    except Exception as e:
        logger.error(f"PDF processing failed: {traceback.format_exc()}")
        return None

def main():
    st.title("Financial Data Extractor")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if uploaded_file:
        try:
            file_bytes = uploaded_file.read()
            
            # Detect tables
            pages_with_tables = detect_tables_in_pdf(file_bytes)
            #st.write(f"Tables detected on pages: {pages_with_tables}")
            
            # Text extraction
            extracted_text = process_pdf(file_bytes, pages_with_tables)
            if not extracted_text:
                st.error("No text extracted")
                return
                
            # JSON generation with validation
            try:
                json_output = generate_text_response(extracted_text)
                print(json_output)
                json_output = re.sub(r"```json|\```", "", json_output).strip()

                print(json_output)
                print(type(json_output))
                # Ensure valid JSON format
                if isinstance(json_output, str):
                    json_output = json.loads(json_output)
                    
                st.json(json_output)
                
                
            except json.JSONDecodeError:
                st.error("Generated response is not valid JSON")
            except Exception as e:
                st.error(f"Response generation failed: {str(e)}")
            
        except Exception as e:  # Correct variable name here
            logger.error(traceback.format_exc())
            st.error(f"Processing failed: {str(e)}")  # And here

if __name__ == "__main__":
    main()




