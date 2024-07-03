import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import string
import spacy

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

nlp = spacy.load("en_core_web_sm")

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

def tokenize_and_lemmatize(text):
    # Remove punctuation
    text_no_punct = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize the text
    tokens = word_tokenize(text_no_punct.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    
    return lemmas

def pos_tagging(lemmas):
    # Perform POS tagging
    pos_tags = pos_tag(lemmas)
    
    return pos_tags

def ner_recognition(text):
    # Perform NER
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    
    return entities

#replace with local file #file_path = "C:\\Users\\abhin\\OneDrive\\Desktop\\report pdf.pdf"
result = extract_text_from_pdf(file_path)
if result:
    lemmas = tokenize_and_lemmatize(result)
    pos_tags = pos_tagging(lemmas)
    print("POS Tags:", pos_tags)
    entities = ner_recognition(result)
    print("Named Entities:", entities)
else:
    print("No text extracted from the PDF file.")
