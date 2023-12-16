import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import fasttext.util
import re
import string
from unidecode import unidecode
import nltk

nltk.download('punkt')
nltk.download('stopwords')
def tokens_to_embeddings(tokens, model):
    # Filter out tokens not in the vocabulary
    filtered_tokens = [token for token in tokens if token in model.words]
    if not filtered_tokens:
        return None  # Return None for documents with no valid tokens
    return sum(model[token] for token in filtered_tokens) / len(filtered_tokens)
def clean_text(text):
    pattern = r'[^\w\s]+'
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('\w*\d\w*', ' ', text)
    text = re.sub(r'\w\'', ' ', text)
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
        text = text.replace(' ' + char + ' ', ' ')
    text = re.sub(r'\b\w{1,3}\b', '', text)  # remove words up to 3 letters
    text = ' '.join(word for word in text.split() if len(word) <= 20)
    text = text.replace('\n', ' ')  # Remove any remaining newline characters

    stop_words = set(stopwords.words('french'))
    # Tokenize the text into words
    words = text.split()
    # Remove stopwords
    words = [word for word in words if word.isalnum() and word not in stop_words]
    # Join the cleaned words back into a string
    cleaned_text = ' '.join(words)

    return cleaned_text
def normalize_vector(vector):
    magnitude = np.linalg.norm(vector)
    if magnitude > 0:
        return vector / magnitude
    else:
        return vector

print("Recommandation de Formations")
input_text = input("Enter your text: ")

fasttext.util.download_model('fr', if_exists='ignore')
pretrained_model = fasttext.load_model('cc.fr.300.bin')

####################dataframe############################
df = pd.read_csv('df.csv')
df['Combined_Text'] = df.apply(lambda row: ' '.join(row), axis=1)   #combine data to one column
df['tokens'] = df['Combined_Text'].apply(nltk.word_tokenize)        #tokenizing
df['embeddings'] = df['tokens'].apply(lambda tokens: tokens_to_embeddings(tokens, pretrained_model))

   #Apply the token-to-embedding

####################user############################

if input_text != '':
    input_text = clean_text(input_text)
    user_input_tokens = nltk.word_tokenize(input_text)
    user_input_embedding_normalized = pretrained_model.get_sentence_vector(" ".join(user_input_tokens))
    magnitude_normalized = np.linalg.norm(user_input_embedding_normalized)
    user_input_embedding_non_normalized = user_input_embedding_normalized * magnitude_normalized
    user_input_embedding = normalize_vector(user_input_embedding_non_normalized)

    ####################similarity############################
    df['cosine_similarity'] = df['embeddings'].apply(lambda x: cosine_similarity([user_input_embedding], [x])[0][0])
    df = df.sort_values(by='cosine_similarity', ascending=False)

    top_N_recommendations = df.head(1)
    print("Recommended Courses:")
    for index, row in top_N_recommendations.iterrows():
        print(row['course_name'])


