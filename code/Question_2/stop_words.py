import csv
import nltk
from nltk.tokenize import word_tokenize

def remove_stopwords(tokens):
    stopwords = nltk.corpus.stopwords.words('english')
    cleaned_tokens = [token for token in tokens if token.lower() not in stopwords]
    return cleaned_tokens

def process_csv(my_file):
    # Initialize an empty string to collect all the text from the file
    all_text = ""

    # Open and read the CSV file
    with open(my_file, mode="r", encoding="utf-8") as token_file:
        reader = csv.reader(token_file)

        for row in reader:
            all_text += " " + row[0]  # Add space to separate texts from 
            # different rows

    tokens = word_tokenize(all_text)

    # Remove stopwords from the tokens
    cleaned_tokens = remove_stopwords(tokens)

    print("Removed stopwords:\n", cleaned_tokens)

my_file = "../giannis_data.csv"
process_csv(my_file)

