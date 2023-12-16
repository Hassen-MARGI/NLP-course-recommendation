import os
import docx
import numpy as np
import pandas as pd
import re
import string
from unidecode import unidecode

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    return text
def process_folder(folder_path):
    folder_name = os.path.basename(folder_path)
    files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]

    folder_text = ""
    for file in files:
        file_path = os.path.join(folder_path, file)
        folder_text += extract_text_from_docx(file_path) + " "

    folder_text = clean_text(folder_text)

    return pd.DataFrame({"course_name": [folder_name], "Description": [folder_text]})


def clean_text(text):
    pattern = r'[^\w\s]+'
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub(r'\w\'', '', text)
    text = re.sub(pattern, ' ', text)
    text = text.replace('\u2019', ' ')  # Remove single quotes (Unicode: ’)
    text = text.replace('\u0027', ' ')  # Remove single quotes (Unicode: ')
    text = text.replace('\u2018', ' ')  # Remove single quotes (Unicode: ‘)
    text = text.replace('\u201c', ' ')  # Remove double quotes (Unicode: “)
    text = text.replace('\u201d', ' ')  # Remove double quotes (Unicode: ”)
    text = text.replace('\u002c', ' ')  # Remove commas (Unicode: ,)
    text = text.replace('\u005C', ' ')  # Remove backslashes (Unicode: \)
    text = text.replace('product', ' ')  # Remove backslashes (Unicode: \)
    text = unidecode(text)
    for char in string.ascii_lowercase:
        text = text.replace(' '+char+' ', ' ')
    text = re.sub(r'\b\w{1,3}\b', '', text)  # remove words up to 3 letters
    text = ' '.join(word for word in text.split() if len(word) <= 20)
    text = text.replace('\n', ' ')  # Remove any remaining newline characters
    return text


data = pd.DataFrame(columns=['course_name', 'Description'])

for folder in os.listdir("courses"):
    folder_path = os.path.join("courses", folder)
    if os.path.isdir(folder_path):
        df = process_folder(folder_path)
        data = pd.concat([data, df], ignore_index=True)
data.to_csv('df.csv', index=False)