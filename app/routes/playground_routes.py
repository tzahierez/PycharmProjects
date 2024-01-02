import os
import PyPDF2
from openai import OpenAI
from flask import Flask, request, jsonify, render_template, Blueprint, current_app

playground_routes = Blueprint('playground', __name__)
api_key = os.getenv("OPENAI_API_KEY")


def split_text_into_chunks(text, chunk_size=1000):
    # Splits the text into chunks, each with a maximum of chunk_size characters
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def summarize_text_chunk(text_chunk):
    prompt = f"Summarize the following text: {text_chunk}"
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()


@playground_routes.route('/summarize_pdf', methods=['GET', 'POST'])
def summarize_pdf():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        # Check if the file has a name
        if file.filename == "":
            return "No selected file"

        # Check if the file is a PDF
        if not file.filename.endswith(".pdf"):
            return "Unsupported file type (PDF only)"

        # Save the uploaded PDF file
        upload_folder = current_app.config['UPLOAD_FOLDER']
        pdf_path = os.path.join(upload_folder, file.filename)
        file.save(pdf_path)

        # Extract text from PDF
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()

        # Check if text extraction was successful
        if not text:
            return "Failed to extract text from PDF"

        # Use OpenAI to summarize the PDF content
        try:
            # Split the text into manageable chunks
            text_chunks = split_text_into_chunks(text)

            # Summarize each chunk
            summaries = [summarize_text_chunk(chunk) for chunk in text_chunks]

            # Combine summaries
            combined_summary = ' '.join(summaries)
            print(combined_summary)
        except Exception as e:
            return f"An error occurred: {str(e)}"

        return render_template("pdf_summary_result.html", summary=combined_summary)

    return render_template("pdf_upload.html")

# Add the rest of your Flask application setup here if needed
