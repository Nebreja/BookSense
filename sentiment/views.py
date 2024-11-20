import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import UploadedFile
from docx import Document
import os
import fitz
import re
from django.core.paginator import Paginator

from django.shortcuts import render

def home_view(request):
    return render(request, "home.html")

# Path to the existing dataset
dataset_file_path = 'D:/wamp64/www/Final_Project/explicit_words_dataset_with_age_suitability.csv'

# Load dataset once into memory
def load_dataset():
    with open(dataset_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        dataset = list(reader)  # Read the dataset into a list of dictionaries
    return dataset


# View function for file upload and analysis
# View function for file upload and analysis
def file_upload_view(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        uploaded_instance = UploadedFile(file=uploaded_file)
        uploaded_instance.save()
        uploaded_file_path = uploaded_instance.file.path
        
        extracted_text = ""
        
        if uploaded_file.content_type == 'text/csv':
            try:
                with open(uploaded_file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    data = list(reader)
                # Paginate CSV data
                paginator = Paginator(data, 10)  # Show 10 items per page
                page_number = request.GET.get('csv_page')
                page_obj = paginator.get_page(page_number)
                return render(request, "result.html", {"data": page_obj})
            except Exception as e:
                return HttpResponse(f"Error reading CSV: {e}", status=400)
        
        elif uploaded_file.content_type == 'application/pdf':
            extracted_text = extract_pdf_text(uploaded_file_path)
        elif uploaded_file.content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            extracted_text = extract_docx_text(uploaded_file_path)

        if not extracted_text:
            return HttpResponse("Failed to extract text from the uploaded file.", status=400)

        # Analyze the extracted text for inappropriate words
        analysis_result = check_suitability(extracted_text)
        
        # Paginate analysis results
        paginator = Paginator(analysis_result, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Return the results to the template
        return render(request, "result.html", {"analysis_result": page_obj})

    return render(request, "upload.html")

def check_suitability(extracted_text):
    dataset = load_dataset()
    unsuitable_words = []

    for row in dataset:
        word = row['Word'].strip()  # Strip any leading/trailing spaces
        # Create a regex pattern to match the word with word boundaries, making sure it handles variations like punctuation
        pattern = r'\b' + re.escape(word) + r'\b'  # Use word boundaries to match whole words
        if re.search(pattern, extracted_text, re.IGNORECASE):
            unsuitable_words.append({
                'word': word,
                'category': row['Category'],
                'language': row['Language'],
                'age_suitability': row['Age_Suitability']
            })

    if unsuitable_words:
        return unsuitable_words
    else:
        return "No explicit words detected."


    
def extract_pdf_text(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    # Initialize an empty string to store extracted text
    extracted_text = ""
    
    # Iterate over each page of the PDF
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        extracted_text += page.get_text()

    # Close the document
    document.close()

    return extracted_text
def extract_docx_text(docx_path):
    doc = Document(docx_path)
    extracted_text = ""
    
    for paragraph in doc.paragraphs:
        extracted_text += paragraph.text

    return extracted_text
