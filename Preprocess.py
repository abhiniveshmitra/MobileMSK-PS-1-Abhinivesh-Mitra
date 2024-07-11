from pypdf import PdfReader
import re
import os

# Define the file path
pdf_file_path = r'c:\Users\abhin\OneDrive\Desktop\medica sbc example.pdf'

# Initialize the PdfReader
reader = PdfReader(pdf_file_path)

# Extract the first page content
important_questions_page = reader.pages[0]
text = important_questions_page.extract_text()
text = text.split("Why This Matters:")[1]
lines = text.split(u"\xa0")
data = []
temp_dict = dict()

# Process the extracted text
for ind, line in enumerate(lines):
    temp_line = line.replace("\n", " ").strip()

    if ind % 2 == 0:
        split_line = temp_line.split("?")

        if len(split_line) != 2:
            break

        temp_dict['question'] = split_line[0].strip() + "?"
        temp_dict['answer'] = split_line[1].strip()
    else:
        temp_dict['detail'] = temp_line
        data.append(temp_dict)
        temp_dict = dict()

# Get the directory and filename for saving the text file
directory, pdf_filename = os.path.split(pdf_file_path)
txt_filename = os.path.splitext(pdf_filename)[0] + "_important_questions.txt"
txt_file_path = os.path.join(directory, txt_filename)

# Save the processed data to a text file
with open(txt_file_path, "w") as f:
    for item in data:
        f.write("### Question\n")
        f.write(item['question'] + "\n")
        f.write("### Answer\n")
        f.write(item['answer'] + "\n")
        f.write("\tFurther Details: ")
        f.write(item['detail'] + "\n")
        f.write("\n\n")

def split_question_rest(line):
    pat = re.compile(r"[a-z]([A-Z])")
    
    for match in pat.finditer(line):
        return line[:match.start() + 1].strip(), line[match.start() + 1:].strip()

    return line.strip(), ""

def split_service_network(line):
    pat = re.compile(r"(\)|[a-z])\s*[A-Z0-9]")

    for match in pat.finditer(line):
        return line[:match.start() + 1].strip(), line[match.start() + 1:].strip()

    return line.strip(), ""

# Process additional pages
data = []

for page_number in range(1, 5):
    page = reader.pages[page_number]
    text = page.extract_text()
    text = "If you" + "If you".join(text.split("If you")[1:])
    text = text.replace("\n", " ")
    lines = text.split(u"\xa0")
    i = 0
    current_is_common_lim_section = False

    while i < len(lines):
        line = lines[i].strip()
        temp_dict = dict()

        if line.startswith("If you"):
            temp_dict['question'], rest = split_question_rest(line)
            temp_dict['service'], temp_dict['network'] = split_service_network(rest)
        else:
            temp_dict['question'] = data[-1]['question']
            temp_dict['service'], temp_dict['network'] = split_service_network(line)

        try:
            temp_dict['non_network'] = lines[i + 1]
            temp_dict['limitations'] = lines[i + 2]
        except IndexError:
            break

        data.append(temp_dict)
        i += 3

# Append the processed data to the text file
with open(txt_file_path, "a") as f:
    for item in data:
        f.write("### Question\n")
        f.write(item['question'] + " for " + item['service'] + "\n")
        f.write("### Answer\n")
        f.write("\tNetwork provider: " + item['network'] + "\n")
        f.write("\tNon-Network provider: " + item['non_network'] + "\n")
        f.write("\tLimitations: " + item['limitations'] + "\n")
        f.write("\n\n")
