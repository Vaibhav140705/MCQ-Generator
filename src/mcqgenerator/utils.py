import os
import traceback
import ast
import json
import PyPDF2
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import re


def clean_pdf_text(text):
    # Remove weird line breaks and multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip unnecessary non-ascii characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def read_file(file):
    text = ""

    if file.name.endswith(".pdf"):
        # 1. Try direct text extraction
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        # 2. If no text, fallback to OCR
        if not text.strip():
            images = convert_from_path(file, dpi=300)
            for img in images:
                text += pytesseract.image_to_string(img)

        # 3. Final cleanup
        text = clean_pdf_text(text)

        if not text.strip():
            raise ValueError("PDF has no readable text (even after OCR).")

    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
        text = clean_pdf_text(text)

    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")

    return text






# def get_table_data(quiz_str):
#     try:
#         if not quiz_str or not quiz_str.strip():
#             raise ValueError("Empty quiz string received")

#         try:
#             quiz_dict = json.loads(quiz_str)
#         except json.JSONDecodeError:
#             # fallback if model returns Python dict-like string
#             quiz_dict = ast.literal_eval(quiz_str)

#         quiz_table_data = []
#         for key, value in quiz_dict.items():
#             mcq = value["mcq"]
#             # options = " || ".join([f"{opt}-> {val}" for opt, val in value["options"].items()])
#             # correct = value["correct"]
#         # Ensure options is a dict
#         options = value["options"]
#         if isinstance(options, str):  
#             try:
#                 options = json.loads(options)  # if it's JSON string
#             except:
#                 import ast
#                 options = ast.literal_eval(options)  # if it's Python-style dict

#             options_str = " || ".join(
#                 [f"{opt}-> {opt_val}" for opt, opt_val in options.items()]
#             )

#             correct = value["correct"]
#             quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
#         return quiz_table_data

#     except Exception as e:
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return None


def clean_quiz_output(quiz_str: str) -> str:
    # Keep only the JSON part (first { to last })
    if "{" in quiz_str and "}" in quiz_str:
        quiz_str = quiz_str[quiz_str.find("{"): quiz_str.rfind("}")+1]
    return quiz_str


def get_table_data(quiz_str):
    import json, ast, traceback
    try:
        quiz_str = clean_quiz_output(quiz_str)
        # First, try to load as proper JSON
        quiz_dict = json.loads(quiz_str)
    except Exception:
        try:
            # If it looks like Python dict (single quotes), try literal_eval
            quiz_dict = ast.literal_eval(quiz_str)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise ValueError("Failed to parse quiz data (check PDF content or model output).")

    quiz_table_data = []

    for key, value in quiz_dict.items():
        mcq = value.get("mcq", "")
        options = value.get("options", {})

        # Fix case where options is string
        if isinstance(options, str):
            try:
                options = json.loads(options)
            except:
                import ast
                options = ast.literal_eval(options)

        correct = value.get("correct", "")

        quiz_table_data.append({
            "MCQ": mcq,
            "Choices": options,   # dict, not string
            "Correct": correct
        })

    return quiz_table_data


