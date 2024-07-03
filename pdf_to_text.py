import PyPDF2

def extract_text_from_pdf(file_path):
    try:
        pdf_file_obj = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        pdf_file_obj.close()
        return text
    except Exception as e:
        print(f"An error occurred: {e}")

# replace with local file #file_path = "C:\\Users\\abhin\\OneDrive\\Desktop\\report pdf.pdf"
result = extract_text_from_pdf(file_path)
if result:
    print(result)
else:
    print("No text extracted from the PDF file.")
