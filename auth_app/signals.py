import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CV_Model
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

@receiver(post_save, sender=CV_Model)
def extract_text_from_cv(sender, instance, **kwargs):
    # Extract text based on the file type
    file_path = instance.cv_file.path

    if file_path.endswith('.pdf'):
        instance.cv_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(('.png', '.jpg', '.jpeg')):
        instance.cv_text = extract_text_from_image(file_path)
    else:
        instance.cv_text = "Unsupported file format"

    # Save the extracted text to the database
    instance.save()

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"
